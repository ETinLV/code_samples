import re


class PasswordValidation:
    """Validate a password contains at least 1 uppercase letter, 1 lowercase letter, is at east 12 chars long 
        and does not contain the string '123' """

    @staticmethod
    def strong_password(strong_password):
        if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*)(?!.*123)(?=.{12}).+$', strong_password):
            return True
        return False


class CropRatio:
    """Return he proportion of single crop vs total crop weight """

    def __init__(self):
        self._crops = {}
        self._total_weight = 0

    def add(self, name, crop_weight):
        if name not in self._crops:
            self._crops[name] = crop_weight
        else:
            self._crops[name] += crop_weight
        self._total_weight += float(crop_weight)

    def proportion(self, name):
        if name not in self._crops:
            return 0
        return self._crops[name] / self._total_weight


class CategoryTree:
    """Return all children of parent. Attempting to add child when category already exists, 
        or add parent that does not exist, raise key error"""

    def __init__(self):
        self.categories = {}

    def add_category(self, category, parent):
        # If category is already a child or parent, raise key error
        if category not in self.categories.keys() and category not in [c for p in self.categories.values() for c in p]:
            if parent:
                self.categories[parent] += category
            else:
                self.categories[category] = []
        else:
            raise KeyError

    def get_children(self, parent):
        return self.categories[parent]
