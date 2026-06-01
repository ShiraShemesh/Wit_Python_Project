from fastapi import UploadFile
from analyzer import CodeAnalyzer

class AnalyzerService:

    @staticmethod
    async def analyze_uploaded_files(files: list[UploadFile]):
        """
        שירות שמקבל רשימת קבצים, קורא את התוכן שלהם ומריץ עליהם את ה-Analyzer.
        מחזיר רק את רשימת הבעיות — משמש את ה-endpoint /alerts
        """
        result = await AnalyzerService.analyze_uploaded_files_full(files)
        return result["issues"]

    @staticmethod
    async def analyze_uploaded_files_full(files: list[UploadFile]):
        """
        שירות שמקבל רשימת קבצים, קורא את התוכן שלהם ומריץ עליהם את ה-Analyzer.
        מחזיר מילון מלא עם issues ו-function_lengths — משמש את ה-endpoint /analyze
        """
        all_issues = []
        all_function_lengths = []

        for file in files:
            contents = await file.read()
            code_content = contents.decode("utf-8")

            # הפעלת מנוע ה-AST
            analyzer = CodeAnalyzer(code_content, filename=file.filename)
            analysis_result = analyzer.analyze()

            all_issues.extend(analysis_result["issues"])
            all_function_lengths.extend(analysis_result["function_lengths"])

        return {
            "issues": all_issues,
            "function_lengths": all_function_lengths
        }