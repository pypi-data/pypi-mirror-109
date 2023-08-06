


class Transposition(object):
    """
    Main idea is call a function that converts
    a structure to a flat array returning a structure 
    back from flat array
    """
    def __init__(self) -> None:
        self.flat_array = {}
        self.new_struct = {}

    def is_dict(self, struct: any) -> None:
        """
        Check is structure dict or not
        """
        if not isinstance(struct, dict):
            raise Exception(
                "This is not dict type, try to change type of structure"
                )
    
    def has_nesting(self, entity: any):
        """
        Check is entity has nesting structure or not
        """
        return isinstance(entity, dict)

    def struct_to_array(self, struct: dict, chain: str="") -> dict:
        """
        Calling recursively of nested structure
        and storing parent-child relationship to chain
        """
        self.is_dict(struct)

        for k, v in struct.items():
            if self.has_nesting(v):
                self.struct_to_array(
                    v, f"{chain}.{k}" if chain else k
                )
            else:
                self.flat_array.update(
                    {f"{chain}.{k}" if chain else k : v}
                )

        return self.flat_array

    def recursion_split(self, k: str, v: any, out: dict) -> None:
        """
        Calling recursively keys of a structure
        to break them on '.' delimiter
        """
        k, *rest = k.split('.', 1)
        if rest:
            self.recursion_split(rest[0], v, out.setdefault(k, {}))
        else:
            out[k] = v

    def array_to_struct(self, flat_array: dict) -> dict:
        """
        For each key of structure calling recursion method
        which will split keys to form recursively nested 
        dictionary
        """
        for k, v in flat_array.items():
            self.recursion_split(k, v, self.new_struct)
        
        return self.new_struct