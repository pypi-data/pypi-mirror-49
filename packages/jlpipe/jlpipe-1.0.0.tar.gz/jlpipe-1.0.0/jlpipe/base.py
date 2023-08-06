# -*- coding: utf-8 -*-
import json
import click
import sys


class MetaStreamCommand(type):
    def __new__(cls, name, bases, attrs):
        attrs.setdefault("abstract", False)
        options = attrs.pop("options", [])
        cls = super().__new__(cls, name, bases, attrs)
        if options:
            cls.options = options + getattr(cls, "options", [])
        if cls.abstract:
            return cls

        obj = cls()
        for option in reversed(cls.options):
            option(obj)
        # import ipdb; ipdb.set_trace()
        return click.command(name=cls.__name__)(obj)


class StopStream(Exception):
    pass


class StreamCommand(metaclass=MetaStreamCommand):
    abstract = True

    options = [
        click.option("-i", "--infile", type=click.Path(exists=True)),
        click.option("-o", "--outfile", type=click.Path())
    ]
    # def __new__(cls, **kwargs):
    #     # import ipdb; ipdb.set_trace()
    #     obj = super(StreamCommand, cls).__new__(cls, **kwargs)
    #     return obj()

    def __call__(self, infile=None, outfile=None, **kwargs):
        if infile:
            self.infile = open(infile)
        else:
            self.infile = sys.stdin

        if outfile:
            self.outfile = open(outfile, "w")
        else:
            self.outfile = sys.stdout

        self.__dict__.update(kwargs)
        self.prepare(**kwargs)

        try:
            while True:
                line = self.infile.readline()
                if not line:
                    break
                obj = self.preprocess(line)
                obj = self.process(obj)
                obj is not None and self.write(obj)
        except StopStream:
            pass
        finally:
            self.final()
            self.infile.close()
            self.outfile.close()

    def write(self, obj):
        self.outfile.write(obj)
        self.outfile.write("\n")

    def prepare(self, **kwargs):
        pass

    def preprocess(self, line):
        return line.strip()

    def process(self, obj):
        return obj

    def final(self):
        pass

    def stop(self):
        raise StopStream


class JsonStreamCommand(StreamCommand):
    abstract = True

    def preprocess(self, line):
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            sys.stderr.write("line: %s" % json.dumps(line, ensure_ascii=False))
            raise
