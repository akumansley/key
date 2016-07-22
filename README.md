# key

"Safe" attribute getter operators for python. Useful when exploring data in a REPL for debugging.

## Usage

	import k
	name = k.name(user)

Works on object attributes and string dictionary keys. List indexes, too:

	first_message = k.messages[0](user)

But if it encounters a list with a non-list key, it will map over the list:

	names = k.name(users)
	message_bodies = k.messages.body(users)  # list of lists [[body1, b2], [b3, b4], ..]

If you'd like you can flatten lists of lists:
	
	mbs = k.messages(flatten=True).body(users)  # list [body1, b2, b3, b4, ..]

If you access a non-present attribute, instead of throwing an exception, it will just return None. This is helpful if objects have heterogeneous attributes.

	coaches = k.coach(users)  # [coach1, None, coach2]

You can combine two `k` instances with + and it will merge them into a dictionary keyed by the path.

	(k.first_name + k.last_name)(users)  # [{'first_name':'foo', 'last_name':'bar'}, ..]

`k._` will return 'self', which can be helpful when doing combinations.

	user = k._ + k.coach.id(user)
