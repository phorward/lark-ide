from . import html5
from lark import Lark
from lark.tree import Tree


class App(html5.Div):
	def __init__(self):
		super().__init__("""
			<h1>
				<img src="lark-logo.png"> IDE
			</h1>
			
			<textarea [name]="grammar" placeholder="Enter Lark Grammar..."></textarea>
			<textarea [name]="input" placeholder="Enter Parser input..."></textarea>
			<ul [name]="ast" />
		""")
		self.sinkEvent("onKeyUp")

		self.grammar["value"] = """
?start: sum
      | NAME "=" sum    -> assign_var
      
?sum: product
    | sum "+" product   -> add
    | sum "-" product   -> sub
    
?product: atom
    | product "*" atom  -> mul
    | product "/" atom  -> div
    
?atom: NUMBER           -> number
     | "-" atom         -> neg
     | NAME             -> var
     | "(" sum ")"
     
%import common.CNAME -> NAME
%import common.NUMBER
%import common.WS_INLINE
%ignore WS_INLINE
""".strip()

		self.input["value"] = "1 + 2 * 3 + 4"
		self.onKeyUp(None)

	def onKeyUp(self, e):
		l = Lark(self.grammar["value"])

		try:
			ast = l.parse(self.input["value"])
		except Exception as e:
			self.ast.appendChild(
				html5.Li(str(e)), replace=True
			)

		print(ast)
		traverse = lambda node: html5.Li([node.data, html5.Ul([traverse(c) for c in node.children])] if isinstance(node, Tree) else node)
		self.ast.appendChild(traverse(ast), replace=True)
