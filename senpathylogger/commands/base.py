# Written By Mohit Daga, CSE Dept. IIT Madras
# For PG Senpathy Computer Center, IIT Madras
# mohit@cse.iitm.ac.in


"""The base command."""
class Base(object):
    """A base command."""

    def __init__(self, options, *args, **kwargs):
        print "ok I was here"
        print options
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def run(self):
        raise NotImplementedError('You must implement the run() method yourself!')
