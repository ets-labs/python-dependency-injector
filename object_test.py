from dependency_injector import providers


object1 = providers.Object(1)
object2 = providers.Object(2)
object3 = providers.Object(3)

# 1

assert object1() == 1

# 2

object1.override(object2)
assert object1() == 2

# 3

object2.override(object3)
assert object1() == 3

print('Success')
