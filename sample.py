class MyClass:
    def method_a(self):
        self.method_b()
        self.method_c()

    def method_b(self):
        self.method_d()

    def method_c(self):
        self.method_e()
        self.method_d()
        self.method_a()

    def method_d(self):
        self.method_e()

    def method_e(self):
        pass

if __name__ == "__main__":
    obj = MyClass()
    obj.method_a()