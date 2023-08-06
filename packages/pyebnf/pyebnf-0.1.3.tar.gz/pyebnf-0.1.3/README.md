# Py-EBNF

**Py-EBNF** is a simple EBNF parser compiler. It can read source code written in a dialect of EBNF and output a parser that can generate a parse tree from conforming input.

Usage (CLI):

    python3 -m pyebnf.compiler source

The output will need to have **pyebnf** in its import path, as the Parser will use primitives and a ParserBase defined in **pyebnf**.

I built this library based on the information at [wikipedia](https://en.wikipedia.org/wiki/Extended_Backus–Naur_Form) on the subject. I used this project as a learning exercise, and therefore decided not to do much research on EBNF compiler creation.

## Concerns

The primitives for this EBNF parser will not work properly with head recursion. E.G. a rule like:

    expression = number
               | expression , operator , number ;

Would result in infinite recursion. However, a rule like:

    expression = number
               | number , operator , expression ;

Will work just fine.

## Dialect

**pyebnf** implements a dialect of EBNF very similar to that presented in the wikipedia article. The one major distinction is I've implemented two concatenation operators: `,` and `.`. `,` is a whitespace-ignoring concatenation operator, it will consume all whitespace at the beginning of the source portion it is working on. `.` on the other hand will no automatically consume whitespace and leaves that to the included rules. I added this because ignoring whitespace is such a common thing in so many programming languages that it would require a really messy grammar definition if whitespace weren't ignored. The initial implementation ignored all whitespace in a different way that was not controllable from the source level. This alternative has worked much better.

Py-EBNF is self-hosting. I initially hand-wrote a parser to understand EBNF, and then used that parser to generate a parser from an EBNF EBNF. You can see the full grammar that generated the parser [here](tests/fixtures/ebnf.ebnf).

## Operators

Operator | Associativity | Precedence | Description
:------: | :------------ | ---------: | :----------
=        | Left          | 1          | Assignment
\|       | Left          | 2          | Alternation
.        | Left          | 3          | Concatenation
,        | Left          | 4          | Whitespace-ignoring concatenation
-        | Left          | 5          | Exclusion
*        | Left          | 6          | Repetition (exact count)
+        | Left          | 7          | Repeat (once or more)

## Directives

**pyebnf** recognizes several directives that will control the source code that is generated.

Directives are lines in comments `(* ... *)` that start with `! ` and take the format `! name key1=value1 key2=value2 ...`. Directives are split on whitespace.

All directives are optional and just serve to override default behavior. Recognized directives:

Name | N   | Description | Arg Name | Arg Description
:--- | :-: | :---------- | :------- | :--------------
rule | \* | Controls rule output | name       | The name of the targeted rule.
"    | "  | "                    | transform  | How to alter the output. The valid arguments are: retype, compress and identity. Retype just changes the type of the generated node. Compress pulls all the descendants together so that the resulting node contains just a single string value. Identity leaves the node unchanged. The default is retype.
"    | "  | "                    | to_type    | When a node is retyped or compressed you can change its type. By default the type is TokenType.{rule_name}, but you can make it whatever text you want with the to_type parameter.
parse_base | ? | Base class for parser | value | The base class name. Defaults to PB.ParserBase where PB is pyebnf.parser_base.
entry_point | ? | Set custom entry point for parser | value | The name of the rule to serve as the entry point for Parser.parse. By default, it is the first rule name encountered.
import | * | Custom imports to parser source | value | Literal import text.

In this table **N** is the number of times the directive should appear. `*` means "zero or more", `+` means "one or more", `?` means "zero or one".

Example directives:

	#! parser_base value=MyParserBase
	#! import value=from\ mylib.ParserBase\ import\ MyParserBase
	#! entry_point value=program

	#! rule name=program transform=retype
	#! rule name=identifier transform=compress


## Special Handling

EBNF defines a group of `? ... ?` as "Special Handling" meaning that the contents are specially interpreted by the underlying code. PyEBNF expects the contents of a special handling to be an identifier, and will handle in one of two ways. If the identifier is one of: get\_ascii\_letter, get\_ascii\_lowercase, get\_ascii\_uppercase, get\_digit, get\_hexdigit, get\_octdigit, get\_printable, get\_punctuation, get\_whitespace the handler will be the function by the same name defined in pyebnf.parser_base. These are short cuts for common character classes.

If the identifier is not one of those, it will be interpreted as a function name on the parser, and will need to be implemented by you.
