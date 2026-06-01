import ast


class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self, code_content: str, filename: str = "unknown"):
        self.code = code_content
        self.filename = filename
        self.issues = []
        self.function_lengths = []

    MAXIMUM_LINES_IN_FILE = 200
    MAXIMUM_LENGTH_IN_FUNC = 20

    def analyze(self):
        lines = self.code.splitlines()

        # 1. בדיקת אורך קובץ
        if len(lines) > self.MAXIMUM_LINES_IN_FILE:
            self.issues.append({
                "file": self.filename,
                "type": "File Length",
                "message": f"The file: {self.filename} too long"
            })

        try:
            tree = ast.parse(self.code)
            self.visit(tree)
        except SyntaxError:
            self.issues.append({
                "file": self.filename,
                "type": "Syntax Error",
                "message": "Syntax Error"
            })

        return {
            "issues": self.issues,
            "function_lengths": self.function_lengths
        }

    def visit_FunctionDef(self, node):
        # 2. בדיקת אורך פונקציה
        func_length = node.end_lineno - node.lineno + 1
        self.function_lengths.append(func_length)

        if func_length > self.MAXIMUM_LENGTH_IN_FUNC:
            self.issues.append({
                "file": self.filename,
                "type": "Function Length",
                "message": f"The function: {node.name} too long ({func_length} lines)"
            })

        # 3. בדיקת חוסר בתיעוד (Docstring)
        if ast.get_docstring(node) is None:
            self.issues.append({
                "file": self.filename,
                "type": "Missing Docstring",
                "message": f"The function: {node.name} missing docstring"
            })

        # 4. בדיקת משתנים שלא בשימוש (Unused Variables) בתוך הפונקציה
        assigned_vars = set()
        used_vars = set()

        # עוברים על כל מה שנמצא בתוך הפונקציה הנוכחית
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.Name):
                if isinstance(sub_node.ctx, ast.Store):  # משתנה שקיבל ערך (למשל x = 5)
                    assigned_vars.add(sub_node.id)
                elif isinstance(sub_node.ctx, ast.Load):  # משתנה שקראו לו (למשל print(x))
                    used_vars.add(sub_node.id)

        # משתנים שהוגדרו אך לא נעשה בהם שימוש
        unused_vars = assigned_vars - used_vars
        for var in unused_vars:
            self.issues.append({
                "file": self.filename,
                "type": "Unused Variable",
                "message": f"המשתנה '{var}' הוגדר בפונקציה '{node.name}' אך לא נעשה בו שימוש"
            })

        self.generic_visit(node)
