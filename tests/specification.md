# Specification

## Documentation Overview

This is the documentation space for the SRL Query Language. We're trying our best to give you a complete overview about what's possible. Please read through these basic syntax rules first:

SRL is case insensitive. Thus, `LITERALLY "test"` is exactly the same as `literally "test"`. But please beware, that everything inside a string is in fact case sensitive. `LITERALLY "TEST"` does NOT equal `literally "test"`.
The comma separating statements is completely optional and has no effect whatsoever. In fact, it gets removed before interpreting. But since it helps the human eye to distinct between different statements, it's allowed.
Strings are interpreted as literal characters and will be escaped. They can either be defined using 'single' or "double" quotation marks. Escaping them using a backslash is possible as well.
Parentheses should only be used when building a sub-query, for example while using a capture or non-capture group to, for example, apply a quantifier to multiple items.
Comments are currently not supported and may be implemented in the future.
In the navigation on the left you can find a few main groups in which all commands can be divided. A short explanation for each group would be:

Characters are everything that matches the string directly. This group contains `letter`, `digit` and `literally`.
Quantifiers are quantifying the statement before. They indicate how often something is allowed to occur.
Groups basically group characters and quantifiers. They are used for applying quantifiers to a whole pattern or to capture and return some specific expressions. Everything in between these groups can be seen as a sub-query.
Lookarounds allow a more complex way of dealing with groups and matches. That way you can define a group to match only if a certain pattern will apply.
Flags apply to the complete query and indicate a specific mode. For instance, setting the `case insensitive` flag, will tell the whole query to ignore case mismatches.
Anchors are pretty easy. They define whether a string must start or end now.

## Characters

Characters are everything that matches the string directly. They are the groundwork to which quantifiers will apply. The syntax always looks as follows:

    character [specification] [quantifier] [others]

As you can see, characters always come first. They start a new statement, and everything that follows defines the previous character. Some characters allow a specification: `letter`, for example, allows you to define a span of allowed letters: `from a to f`

Every character or character set can be quantified. You may want to match exactly four letters `from a to f`. This would match abcd, but not abcg. You can do that by supplying `exactly 4 times` as a quantifier:

SRL Builder:

    >>> from srl.builder import Builder
    >>> builder = Builder()
    >>> query = builder.letter('a', 'f').exactly(4)
    >>> print query.get()
    [a-f]{4}
    >>> query.is_matching('abcd')
    True

Okay, let's dive into the different characters. Below, you can find a list of all available characters along with an example query.

### literally

    literally "string"

The `literally` character allows you to pass a string to the query that will be interpreted as exactly what you've requested. Nothing else will match, besides your string. Any special character will automatically be escaped. The sample code matches, since the test string contains "sample". Try removing it.

    >>> builder = Builder()
    >>> query = builder.literally("sample")
    >>> print query.get()
    (?:sample)
    >>> query.findall('this is a sample')
    ['sample']
    >>> query.findall('this is a maplecady')
    []

### one of

    one of "characters"

`literally` comes in handy if the string is known. But if there is a unknown string which may only contain certain characters, using `one of` makes much more sense. This will match one of the supplied characters.

    >>> builder = Builder()
    >>> query = builder.oneOf('a%1')
    >>> print query.get()
    [a%1]
    >>> query.is_matching('%')
    True
    >>> query.is_matching('$')
    False

### letter

    letter [from a to z]

This will help you to match a letter between a specific span, if the exact word isn't known. If you know you're expecting an letter, then go for it. If not supplying anything, a normal letter between a and z will be matched. Of course, you can define a span, using the `from x to y` syntax.

Please note, that this will only match one letter. If you expect more than one letter, use a quantifier.

    >>> builder = Builder()
    >>> query = builder.letter('a', 'f')
    >>> print query.get()
    [a-f]
    >>> query.is_matching('a')
    True
    >>> query.is_matching('z')
    False

### any character

    any character

Just like a letter, `any character` matches anything between A to Z, 0 to 9 and `_`, case insensitive. This way you can validate if someone for example entered a valid username.

    >>> builder = Builder()
    >>> query = builder.startWith().anyCharacter().onceOrMore().mustEnd()
    >>> print query.get()
    ^\w+$
    >>> query.is_matching('aBcD0_1')
    True
