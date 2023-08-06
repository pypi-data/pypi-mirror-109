"""TODO doc"""

import itertools
import inspect
import hashlib
import re
import sys
import traceback
import textwrap
import uuid
import logging

import xmltodict
import langdetect
import requests
 
from datetime import datetime, timedelta
from functools import partial, reduce

from validate_email import validate_email

__all__=["format_exception", "xml_to_object"]

def format_exception(e):
    exception_list = traceback.format_stack()
    exception_list = exception_list[:-2]
    exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
    exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))

    exception_str = "Traceback (most recent call last):\n"
    exception_str += "".join(exception_list)
    
    # Removing the last \n
    exception_str = exception_str[:-1]

    return exception_str

def format_email(email):
    email = email.replace(" at ", "@")
    email = email.replace(" ", "")
    return email

def isPrimitive(obj):
    return not hasattr(obj, '__dict__')

def parseDatetime(date_string, date_format='%Y-%m-%d %H:%M:%S'):
    for pattern in (date_format, '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S%Z', '%Y-%m-%dT%H:%M:%SZ'):
        try:
            return datetime.strptime(date_string, pattern)
        except Exception as e: pass
    m = re.match(parseDatetime.re_pattern, date_string)
    if m is not None:
        year = int(m.group("year"))
        month = int(m.group("month"))
        day = int(m.group("day"))

        hour = int(m.group("hour")) if m.group("hour") is not None else 0 
        minute = int(m.group("minute")) if m.group("minute") is not None else 0 
        second = int(m.group("second")) if m.group("second") is not None else 0
        
        timezone = m.group("tz")
        
        return datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

    logging.warning("[parseDatetime] Error parsing datetime ({}) with format '{}'".format(date_string, date_format))
    return None
parseDatetime.re_pattern = re.compile('(?P<year>[\d]{2,4})(-|/){1}(?P<month>[\d]{2})(-|/){1}(?P<day>[\d]{2})(\w)?(?P<hour>[\d]{2})?(:)?(?P<minute>[\d]{2})?(:)?(?P<second>[\d]{2})?(?P<tz>[a-zA-Z]+)?')

def roundTime(date_time, roundToSeconds=24*60*60):
    if date_time == None : date_time = datetime.now()
    seconds = (date_time.replace(tzinfo=None) - date_time.min).seconds
    rounding = (seconds+roundToSeconds/2) // roundToSeconds * roundToSeconds
    return date_time + timedelta(0,rounding-seconds,-date_time.microsecond)

def camelCaseToSnakeCase(value, sep='_'):
    return ''.join([sep+c.lower() if c.isupper() else c for c in value]).lstrip(sep)

def snakeCaseToCamelCase(value, sep='_'):
    return ''.join(word.title() for word in value.split(sep))

def is_sha1(str_value, return_sha1_string=False):
    match = re.match(is_sha1.re_sha1, str_value)
    return hashlib.sha1(str_value.encode("utf-8")).hexdigest() if return_sha1_string else (match is not None)
is_sha1.re_sha1 = re.compile(r'\b[0-9a-f]{40}\b')

def to_dict_lowercase(value):
    if not isinstance(value, dict): return value
    my_dict = {}
    for k,v in value.items():
        if isinstance(v, dict):
            my_dict[k.lower()] = to_dict_lowercase(v)
        elif isinstance(v, list):
            for l in v:
                my_dict[k.lower()] = []
                if isinstance(l, dict):
                    my_dict[k.lower()].append(to_dict_lowercase(l))
                else:
                    my_dict[k.lower()].append(l)
        else:
            my_dict[k.lower()] = v
    return my_dict


def tokenize_name(name, remove_punctuation=True, min_terms=-1, left_coincidences=1, hash_token=True):
        rst = None
        if name is None or not isinstance(name,str): return None

        if 0 < min_terms:
            tokens = [n for n in name.split(' ')]
            if remove_punctuation: tokens = [re.sub(r"[\W]+","", t) for t in tokens]
            tokens = [t.strip().lower() for t in tokens if "" != t.strip()]

            if min_terms < len(tokens):
                rst = []
                for r in range(min(min_terms,len(tokens)),len(tokens)+1):
                    for t in itertools.combinations(tokens, r):
                        is_valid = True
                        for i in range(left_coincidences):
                            is_valid = is_valid and (t[i] == tokens[i])
                        
                        if is_valid:
                            candidate = ''.join(t)
                            if hash_token:
                                rst.append(hashlib.sha1(candidate.encode("utf-8")).hexdigest())
                            else:
                                rst.append(candidate.encode("utf-8")) 
            else:
                return tokenize_name(name, remove_punctuation=remove_punctuation)
        else:
            if remove_punctuation:
                _name = re.sub(r"[\W]+","", name)
            _name  = _name.strip().lower()
            if re.match(r"[\w]*,[\w]*", _name):
                _name = ' '.join(reversed(_name.split(',')))

            if hash_token:
                rst = [hashlib.sha1(_name.encode("utf-8")).hexdigest()]
            else:
                rst = [_name.encode("utf-8")]
 
        return rst[0] if -1 == min_terms and len(rst) > 0 else rst

def countWordOcurrences(string, word):
    if string is None or word is None: return 0
    rst = len(re.findall(word, string))
    return rst

def detect_lang(string):
    if not isinstance(string, str): return None
    return langdetect.detect(string)

def is_valid_email(email):
    if email not in is_valid_email.cache:
        kwargs = {
            "check_regex":True, 
            "check_mx":True, 
            "smtp_timeout":10, 
            "dns_timeout":10, 
            "use_blacklist":True, 
            "debug":False
        }
        is_valid_email.cache[email] = validate_email(email_address=email, **kwargs)
    return is_valid_email.cache[email]
is_valid_email.cache = {}

def calculate_sha1_of_file(path):
    f = open(path)
    d = f.read()
    h = hashlib.sha1(str(d).encode("utf-8"))
    h = h.hexdigest()
    return h

def parseHTTPRequestParameters(url, parameter=None):
    query = requests.utils.urlparse(url).query
    params = dict(x.split('=') for x in query.split('&'))
    return params[parameter] if parameter is not None else params

def injectPatchIntoMethod(p_clazz, p_method, p_patch):
    try:
        if not inspect.isclass(p_clazz): return False
        if not inspect.isfunction(p_patch): return False
        if not isinstance(p_method, str): return False

        my_method = getattr(p_clazz, p_method)
        if not hasattr(p_clazz, p_method): return False
        if not inspect.isfunction(my_method): return False

        name = "z__{}__{}".format(my_method.__name__, p_patch.__name__)
        if hasattr(p_clazz, name): return True

        name_patch = "z_impl_{}".format(p_patch.__name__)
        setattr(p_clazz, name_patch, p_patch)

        src = inspect.getsource(my_method)
        src = textwrap.dedent(src)
        src = src.replace("def {}".format(p_method), "def {}".format(name))
        src = "{source}{indent}self.{patch}()".format(source=src,indent=4*' ', patch=name_patch)

        code = compile(src, "", "exec")
        exec(code)

        code = compile("injectPatchIntoMethod._functions['{name}'] = {name}".format(name=name), "", "exec")
        exec(code)
        setattr(p_clazz,p_method, injectPatchIntoMethod._functions[name])
        
        return True
    except Exception as e: 
        logging.error("[injectPatchIntoMethod] exception injecting ({}, {})".format(p_class.__name__, p_method)) 
        return False
injectPatchIntoMethod._functions = {}

# def injectPatchIntoFunction(p_function, p_patch):
#     try:
#         if not inspect.isfunction(p_function): return False
#         if not inspect.isfunction(p_patch): return False

#         p_module = inspect.getmodule(p_function)
#         if p_module is None: return False

#         name = "z__{}__{}".format(p_function.__name__, p_patch.__name__)
#         if hasattr(p_module, name): return True

#         name_patch = "z_impl_{}".format(p_patch.__name__)
#         setattr(p_module, name_patch, p_patch)

#         src = inspect.getsource(p_function)
#         src = textwrap.dedent(src)
#         src = src.replace("def {}".format(p_function.__name__), "def {}".format(name))
#         src = "{source}{indent}{patch}()".format(source=src,indent=4*' ', patch=name_patch)

#         code = compile(src, "", "exec")
#         exec(code)

#         code = compile("injectPatchIntoFunction._functions['{name}'] = {name}".format(name=name), "", "exec")
#         exec(code)
#         setattr(p_module, p_function.__name__, injectPatchIntoFunction._functions[name])
        
#         return True
#     except Exception as e: logging.error(e)
# injectPatchIntoFunction._functions = {}


class XmlToObjectObject(object):

    def get_attribute_keys(self):
        if not hasattr(self,"_attribute_keys"):
            self._attribute_keys = self.__get_attribute_keys_impl(self,"")
            self._attribute_keys = [a[1:] if a[0] == '/' else a for a in self._attribute_keys]
        return self._attribute_keys

    def get_attributes(self, re_path):
        if re_path is None: return []
        if not isinstance(re_path,str): return []
        if "" == re_path.strip(): return []

        format_re_path = lambda x: "[a-zA-Z0-9_/]{}".format(x) if x in ('*','+','?') else x
        splitted_re_path = re_path.split('/')
        splitted_re_path = [format_re_path(a.strip()) for a in splitted_re_path]

        re_path = '/'.join(splitted_re_path)
        re_pattern = re.compile(re_path)
        re_attrs = list(filter(re_pattern.match, self.get_attribute_keys()))

        rst = []

        if 0 != len(re_attrs):
            valid_term = lambda x: "[a-zA-Z0-9_/]*" != x and "[a-zA-Z0-9_/]?" != x and "[a-zA-Z0-9_/]+" != x
            splitted_re_path = [a for a in splitted_re_path if valid_term(a)]

            re_valid_term = splitted_re_path[-1] if 0!= len(splitted_re_path) else "[a-zA-Z0-9_/]*"
            re_valid_term  = re.compile(re_valid_term)

            for re_attr in re_attrs:
                re_obj = self
                rst_obj = None

                lst_re_attr = re_attr.split('/')
                while 0 != len(lst_re_attr):
                    my_re_attr = lst_re_attr.pop(0)
                    if re_valid_term.match(my_re_attr): 
                        rst_obj = re_obj.__dict__[my_re_attr]
                    re_obj = re_obj.__dict__[my_re_attr]
                if rst_obj is not  None: rst.append(rst_obj)

        return rst

    def get_attribute(self, re_path):
        rst = self.get_attributes(re_path)
        return rst[0] if 0 != len(rst) else None

    def __get_attribute_keys_impl(self,obj,path):
        rst = []
        for attr in obj.__dict__.keys():
            if isPrimitive(obj.__dict__[attr]):
                rst.append("{}/{}".format(path,attr))
            else:
                rst.extend([a for a in self.__get_attribute_keys_impl(obj.__dict__[attr],"{}/{}".format(path,attr))])
        return rst

def xml_to_object(xml, default_class=None, class_mapping=None, prefix_attr="attr_", ignore_namespaces=False, lower_case=False, snake_case=False):
    if xml is None: return None

    my_object = None
    if isinstance(xml,str) or isinstance(xml,bytes):
        my_data = xmltodict.parse(xml)
        my_data = my_data[next(iter(my_data))]
        my_object = _xml_to_object_class(default_class, class_mapping)
        my_rename_func = partial(
            _xml_to_object_rename_key, 
            prefix_attr=prefix_attr, ignore_namespaces=ignore_namespaces, 
            lower_case=lower_case, snake_case=snake_case)
                   
        _xml_to_object_implementation(my_object, my_data, default_class, class_mapping, my_rename_func)
    
    return my_object   

def _xml_to_object_class(default_class, class_mapping):
    if class_mapping is not None and '' in class_mapping:
        my_object = class_mapping['']()
    elif default_class is not None:
        my_object = default_class()
    else:
        my_object = XmlToObjectObject()#type(str(uuid.uuid4().hex).replace('-','_'), (), {})
    return my_object

def _xml_to_object_implementation(my_object, my_data, default_class, class_mapping, rename_func):
    if isinstance(my_data, dict):
        for key,val in my_data.items():
            key = rename_func(key)
            if not isPrimitive(val):
                dict_object = _xml_to_object_class(default_class, class_mapping)
                if val is not None:
                    val = _xml_to_object_implementation(dict_object, val, default_class, class_mapping,rename_func)
            setattr(my_object,key,val)
        return my_object
    elif isinstance(my_data, list):
        lst = []
        for val in my_data:
            lst_object = class_mapping[key]() if key in class_mapping else default_class()
            if val is not None:
                lst_val = _xml_to_object_class(default_class, class_mapping, my_rename_func) 
            lst.append(lst_val)
        return lst
    else:
        a = type(my_data)
        if 'str' != a:
            logging.info(a)
        return my_data

def _xml_to_object_rename_key(key, prefix_attr="attr_", ignore_namespaces=False, lower_case=False, snake_case=False):
    if '@' in key:
        key = key.replace('@','attr_')

    if ignore_namespaces and ':' in key:
        key = key[key.index(':')+1:]
    key = key.replace(':','_')
    
    if snake_case:
        key = ''.join(['_'+c.lower() if c.isupper() else c for c in key]).lstrip('_')

    if lower_case:
        key = key.lower()

    return key


# old code XmlToObjectObject
#     def get_attributes(self, path):
#         rst = []

#         is_valid = lambda x,y: (x == y or y == '*' or y == '...')
#         data =  [(self, [tag.strip() for tag in path.split('/') if tag.strip() != ""])]
#         while 0 != len(data):
#             my_obj,my_path = data.pop(0)
#             my_attrs = [a for a in my_obj.__dict__.keys() if is_valid(a,my_path[0])]

#             for my_attr in my_attrs:
#                 if isPrimitive(my_obj.__dict__[my_attr]):
#                     if 1 == len(my_path):
#                         rst.append(my_obj.__dict__[my_attr])
#                 else:
#                     try:
#                         len_path = len(my_path)
#                         if 1 == len_path:
#                             rst.append(my_obj.__dict__[my_attr])
#                             if '...' == my_path[0]:
#                                 data.append((my_obj.__dict__[my_attr], my_path[0:]))
#                         elif 2 == len_path:
#                             if my_attr == my_path[1] and my_attr != my_path[0]:
#                                 rst.append(my_obj.__dict__[my_attr])
#                             else:
#                                 if '...' == my_path[1]:
#                                     data.append((my_obj.__dict__[my_attr], my_path[1:]))
#                                 elif '*' == my_path[1]:
#                                     rst.append(my_obj.__dict__[my_attr])
#                                 else:
#                                     data.append((my_obj.__dict__[my_attr], my_path[1:]))
#                         else:
#                             if '...' == my_path[0]:
#                                 if '...' == my_path[1]:
#                                     data.append((my_obj.__dict__[my_attr], my_path[1:]))
#                                 elif '*' == my_path[1]:
#                                     my_path[1]=my_path[0] 
#                                     data.append((my_obj.__dict__[my_attr], my_path[1:]))
#                                 else:
#                                     if my_attr == my_path[1]: 
#                                         data.append((my_obj.__dict__[my_attr], my_path[2:]))
#                                     else:
#                                         data.append((my_obj.__dict__[my_attr], my_path[0:]))
#                             elif '*' == my_path[0]:
#                                 if '...' == my_path[1]:
#                                     data.append((my_obj.__dict__[my_attr], my_path[1:]))
#                                 elif '*' == my_path[1]:
#                                     data.append((my_obj.__dict__[my_attr], my_path[1:]))
#                                 else:
#                                     if my_attr == my_path[1]: 
#                                         data.append((my_obj.__dict__[my_attr], my_path[2:]))
#                                     else:
#                                         data.append((my_obj.__dict__[my_attr], my_path[1:]))
#                             else:
#                                 if '...' == my_path[1]:
#                                     data.append((my_obj.__dict__[my_attr], my_path[1:]))
#                                 elif '*' == my_path[1]: 
#                                     data.append((my_obj.__dict__[my_attr], my_path[1:]))
#                                 else:
#                                     data.append((my_obj.__dict__[my_attr], my_path[1:])) 

#                     except Exception as e:
#                         logging.info(e)

#         return [r for r in rst if r is not None]