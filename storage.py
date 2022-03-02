class BrowserStorage:

    def __init__(self, driver, storageName) :
        self.driver = driver
        self.storage_name = storageName

    def __len__(self):
        return self.driver.execute_script("return window." + self.storage_name + ".length;")

    def items(self) :
        return self.driver.execute_script( \
            "var ls = window." + self.storage_name + ", items = {}; " \
            "for (var i = 0, k; i < ls.length; ++i) " \
            "  items[k = ls.key(i)] = ls.getItem(k); " \
            "return items; ")

    def keys(self) :
        return self.driver.execute_script( \
            "var ls = window." + self.storage_name + ", keys = []; " \
            "for (var i = 0; i < ls.length; ++i) " \
            "  keys[i] = ls.key(i); " \
            "return keys; ")

    def get(self, key):
        return self.driver.execute_script("return window." + self.storage_name + ".getItem(arguments[0]);", key)

    def set(self, key, value):
        self.driver.execute_script("window." + self.storage_name + ".setItem(arguments[0], arguments[1]);", key, value)

    def has(self, key):
        return key in self.keys()

    def remove(self, key):
        self.driver.execute_script("window." + self.storage_name + ".removeItem(arguments[0]);", key)

    def clear(self):
        self.driver.execute_script("window." + self.storage_name + ".clear();")

    def __getitem__(self, key) :
        value = self.get(key)
        if value is None :
          raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        return key in self.keys()

    def __iter__(self):
        return self.items().__iter__()

    def __repr__(self):
        return self.items().__str__()