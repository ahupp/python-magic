There are two python modules named 'magic' that do the same thing, but
with incompatible APIs.  One of these ships with libmagic, and (this one) is
distributed through pypi.  Both have been around for many years and have
substantial user bases.  This incompatibility is a major source of pain for
users, and bug reports for me.

To mitigate this pain, python-magic has added a compatibility layer to export
the libmagic python API parallel to the existing one.

The mapping between the libmagic and python-magic functions is:

    detect_from_filename => from_file
    detect_from_content => from_buffer
    detect_from_fobj => from_descriptor(f.fileno())
    open => Magic()


