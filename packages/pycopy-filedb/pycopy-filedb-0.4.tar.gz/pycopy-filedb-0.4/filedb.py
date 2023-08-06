import uos
import utime
import ujson
from ucollections import namedtuple


class DB:

    def __init__(self, name):
        self.name = name

    def connect(self):
        pass

    def close(self):
        pass


class Model:

    @classmethod
    def fname(cls, pkey):
        return "%s/%s/%s" % (cls.__db__.name, cls.__table__, pkey)

    @classmethod
    def mapkeys(cls, obj):
        return [obj.get(k) for k in cls.__fields__]

    @classmethod
    def json2row(cls, obj):
        return cls.Row(*[obj.get(k) for k in cls.__fields__])

    @classmethod
    def create_table(cls, fail_silently=False):
        cls.__fields__ = list(cls.__schema__.keys())
        cls.Row = namedtuple(cls.__table__, cls.__fields__)
        for d in (cls.__db__.name, "%s/%s" % (cls.__db__.name, cls.__table__)):
            try:
                uos.mkdir(d)
            except OSError as e:
                if fail_silently:
                    print(e)
                else:
                    raise

    @classmethod
    def create(cls, **fields):
        pkey_field = cls.__fields__[0]
        pkey_type = cls.__schema__[pkey_field]
        for k, v in cls.__schema__.items():
            if k not in fields:
                default = v[1]
                if callable(default):
                    default = default()
                fields[k] = default

        pkey = fields[pkey_field]
        with open(cls.fname(pkey), "w") as f:
            f.write(ujson.dumps(fields))
        print("create: pkey:", pkey)
        return pkey

    @classmethod
    def get_id(cls, pkey):
        with open(cls.fname(pkey)) as f:
            return [cls.json2row(ujson.loads(f.read()))]

    @classmethod
    def update(cls, where, **fields):
        pkey_field = cls.__fields__[0]
        assert len(where) == 1 and pkey_field in where
        print("update:", where)
        with open(cls.fname(where[pkey_field])) as f:
            data = ujson.loads(f.read())
        data.update(fields)
        with open(cls.fname(where[pkey_field]), "w") as f:
            f.write(ujson.dumps(data))

    @classmethod
    def scan(cls):
        for dirent in uos.ilistdir("%s/%s" % (cls.__db__.name, cls.__table__)):
            fname = dirent[0]
            if fname[0] == ".":
                continue
            with open(cls.fname(fname)) as f:
                yield cls.json2row(ujson.loads(f.read()))


if hasattr(utime, "localtime"):
    def now():
        return "%d-%02d-%02d %02d:%02d:%02d" % utime.localtime()[:6]
else:
    def now():
        return str(int(utime.time()))
