from xpt import ADB, Fastboot

bob = ADB()
jim = Fastboot()
print(bob.is_available())
print(bob.get_version())

print(jim.get_version())