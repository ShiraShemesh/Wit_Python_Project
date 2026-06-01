import io
import zipfile
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import Counter


class GraphService:

    @staticmethod
    def generate_graphs_zip(analysis_result: dict):
        """
        מקבל את תוצאת הניתוח המלאה ומחזיר קובץ ZIP עם כל הגרפים כ-PNG
        """
        issues = analysis_result.get("issues", [])
        function_lengths = analysis_result.get("function_lengths", [])

        graphs = {
            "histogram_function_lengths.png": GraphService._build_histogram(function_lengths),
            "pie_issues_by_type.png":         GraphService._build_pie_chart(issues),
            "bar_issues_by_file.png":         GraphService._build_bar_chart(issues),
        }

        return GraphService._pack_into_zip(graphs)

# גרף 1 : היסטוגרמה
    @staticmethod
    def _build_histogram(function_lengths: list):
        """
        בונה היסטוגרמה של התפלגות אורכי הפונקציות בקבצים שנותחו
        """
        fig, ax = plt.subplots()

        if function_lengths:
            ax.hist(function_lengths, bins=10, color="steelblue", edgecolor="black")
        else:
            ax.text(0.5, 0.5, "No functions found", ha="center", va="center", transform=ax.transAxes)

        ax.set_title("Distribution of Function Lengths")
        ax.set_xlabel("Lines in Function")
        ax.set_ylabel("Number of Functions")

        return GraphService._fig_to_bytes(fig)

#  גרף 2 : עוגה
    @staticmethod
    def _build_pie_chart(issues: list):
        """
        בונה תרשים עוגה המחלק את הבעיות לפי סוג (Function Length, Unused Variable וכו')
        """
        fig, ax = plt.subplots()

        if issues:
            type_counts = Counter(issue["type"] for issue in issues)
            ax.pie(
                type_counts.values(),
                labels=type_counts.keys(),
                autopct="%1.1f%%",
                startangle=140
            )
            ax.set_title("Issues by Type")
        else:
            ax.text(0.5, 0.5, "No issues found ", ha="center", va="center", transform=ax.transAxes)
            ax.set_title("Issues by Type")

        return GraphService._fig_to_bytes(fig)

#גרף 3 : עמודות
    @staticmethod
    def _build_bar_chart(issues: list):
        """
        בונה גרף עמודות המציג כמה בעיות נמצאו בכל קובץ שנותח
        """
        fig, ax = plt.subplots()

        if issues:
            file_counts = Counter(issue["file"] for issue in issues)
            ax.bar(file_counts.keys(), file_counts.values(), color="coral", edgecolor="black")
            ax.set_title("Issues per File")
            ax.set_xlabel("File")
            ax.set_ylabel("Number of Issues")
            plt.xticks(rotation=30, ha="right")
            plt.tight_layout()
        else:
            ax.text(0.5, 0.5, "No issues found ", ha="center", va="center", transform=ax.transAxes)
            ax.set_title("Issues per File")

        return GraphService._fig_to_bytes(fig)


    @staticmethod
    def _fig_to_bytes(fig):
        """
        ממיר Figure של matplotlib לאובייקט BytesIO ומנקה את הזיכרון
        """
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        plt.close(fig)  # שחרור זיכרון — חשוב בסביבת שרת
        buf.seek(0)
        return buf

# אריזת כל הגרפים ל ZIP
    @staticmethod
    def _pack_into_zip(graphs: dict):
        """
        מקבל מילון של {שם_קובץ: BytesIO} ואורז אותם לקובץ ZIP בזיכרון
        """
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for filename, png_bytes in graphs.items():
                zf.writestr(filename, png_bytes.read())
        zip_buffer.seek(0)
        return zip_buffer