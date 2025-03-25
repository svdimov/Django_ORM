# list1 = []  # Empty list
# list2 = None  # None
#
# # Using 'if not'
# if not list1:
#     print("list1 is either None or empty.")  # ✅ This runs because list1 is empty.
#
# if not list2:
#     print("list2 is either None or empty.")  # ✅ This runs because list2 is None.
#
list1 = []  # Empty list
list2 = None  # None

# Using 'is None'
if list1 is None:
    print("list1 is None.")  # ❌ This will NOT run because list1 is an empty list, not None.

if list2 is None:
    print("list2 is None.")  # ✅ This runs because list2 is None.
