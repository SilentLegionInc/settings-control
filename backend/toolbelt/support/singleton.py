class Singleton(type):
    instance = None

    def __call__(cls, *args, **kw):
        if not cls.instance:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        if hasattr(cls.instance, '__call__'):
            cls.instance.__call__()
        return cls.instance
