def main():
    import sys,os
    from subprocess import run
    import pyOfficeSheet,pyOfficeLearn
    print("\r\nwelcome to py-office\r\n")

    if 'sheet' in sys.argv:
        index = sys.argv.index('sheet')
        run([sys.executable,'-m','pyOfficeSheet']+sys.argv[index:])
        return 0 

    if 'learn' in sys.argv:
        index = sys.argv.index('learn')
        run([sys.executable,'-m','pyOfficeLearn']+sys.argv[index:])
        return 0 

    if 'help' in sys.argv or '-help' in sys.argv or '--help' in sys.argv or '-h' in sys.argv:
        print("""Usage: py-office <command> [<option>...]

commands:    description:

    sheet  |  launch py-office-sheet
    
    doc    |  launch py-office-doc
    
    learn  |  launch py-office-learn""")
        return 0

    if 'setup' in sys.argv:
        import pyshortcuts
        from inspect import getfile
        i = sys.platform

        libpath = getfile(pyOfficeSheet).replace('__init__.py','')

        pyshortcuts.make_shortcut(os.path.join(libpath,'__main__.py'), name = 'py-office-sheet',icon=os.path.join(libpath,'pic','icon','py-office-icon_small.png'),terminal = False)

        del pyshortcuts
        import pyshortcuts

        libpath = getfile(pyOfficeLearn).replace('__init__.py','')

        pyshortcuts.make_shortcut(os.path.join(libpath,'__main__.py'), name = 'py-office-learn',icon=os.path.join(libpath,'pic','icon','py-office-icon_small.png'),terminal=False)

        return 0

    print('Usage: py-office <command> [<option>...]')



if __name__ == '__main__':
    main()