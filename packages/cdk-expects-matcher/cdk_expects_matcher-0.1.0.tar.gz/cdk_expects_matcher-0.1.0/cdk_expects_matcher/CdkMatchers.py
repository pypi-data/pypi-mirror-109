import re

from expects.matchers import Matcher

ANY_VALUE = '__ANY_VALUE__'


class have_parameter(Matcher):

    def __init__(self, expected_name: str, expected_props: any):
        self._expected_name = expected_name
        self._props = expected_props

    def _match(self, cfn_template):
        if self._expected_name in cfn_template['Parameters']:
            props = cfn_template['Parameters'][self._expected_name]
            if not self._props:
                return True, ['Cloudformation parameter exists']
            for expected_key in self._props.keys():
                if expected_key in props:
                    if props[expected_key] == self._props[expected_key]:
                        return True, ['Cloudformation parameter exists']

        return False, ["Cloudformation parameter doesn't exist"]


class have_resource(Matcher):
    def __init__(self, expected_type: str, expected_props: any):
        self._type = expected_type
        self._expected = expected_props

    def _match(self, cfn_template):

        found = False

        for resource in cfn_template['Resources'].values():
            all_conditions_met = True
            if resource['Type'] == self._type:
                props = resource['Properties']
                if not self._expected:
                    all_conditions_met &= True
                for expected_key in self._expected.keys():
                    if expected_key in props:
                        print(f' >>>>>>>>> Expected key = {expected_key}')
                        if self._expected[expected_key] == ANY_VALUE:
                            print(f' >>>>>>>> Case1 {self._expected[expected_key]}')
                            all_conditions_met &= True
                        elif type(self._expected[expected_key]) in [str, dict] and ANY_VALUE in self._expected[expected_key]:
                            regex_value = self._expected[expected_key].replace(ANY_VALUE, ".*")
                            print(f' >>>>>>>> Case2 {regex_value}')
                            if re.search(regex_value, props[expected_key]):
                                all_conditions_met &= True
                        elif type(self._expected[expected_key]) == list:
                            print(
                                f' >>>>>>>> Case3 RECURSION list {props[expected_key]} == {self._expected[expected_key]}')
                        elif type(self._expected[expected_key]) == dict:
                            print(
                                f' >>>>>>>> Case4 RECURSION dict {props[expected_key]} == {self._expected[expected_key]}')

                        elif props[expected_key] == self._expected[expected_key]:
                            print(f' >>>>>>>> Case5 {props[expected_key]} == {self._expected[expected_key]}')
                            all_conditions_met &= True
                        else:
                            print(f' >>>>>>>> Case6 {props[expected_key]} == {self._expected[expected_key]}')
                            all_conditions_met &= False
                    else:
                        print(f' >>>>>>>> Case7 {self._expected[expected_key]}')
                        all_conditions_met &= False
            else:
                all_conditions_met &= False

            if all_conditions_met:
                found = True
                break

        if found:
            return True, ["Cloudformation resource exists"]
        else:
            print(f' >>>>>>>> Case8 {self._type} && {self._expected} ')
            return False, ["Cloudformation resource doesn't exist"]
