from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from typing import List, Dict

class PDFGenerator:
    def __init__(self):
        pass

    def generate_report(self, programs: List[Dict[str, str]], output_path: str):
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        # Title
        title = Paragraph(f"Appnort Software Audit Report - {datetime.now().strftime('%Y-%m-%d')}", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Summary Statistics
        total_programs = len(programs)
        
        # Group by Category
        grouped_programs = {}
        for prog in programs:
            cat = prog.get('category', 'Unknown')
            if cat not in grouped_programs:
                grouped_programs[cat] = []
            grouped_programs[cat].append(prog)

        summary_text = Paragraph(f"Total Installed Programs: {total_programs}", styles['Normal'])
        elements.append(summary_text)
        
        # Breakdown
        breakdown_text = "<b>Category Breakdown:</b><br/>"
        for cat, progs in grouped_programs.items():
            breakdown_text += f"{cat}: {len(progs)}<br/>"
        elements.append(Paragraph(breakdown_text, styles['Normal']))
        elements.append(Spacer(1, 12))

        # Risk Legend
        legend_text = (
            "<b>Security Risk Legend:</b><br/>"
            "<font color='green'><b>Low</b></font>: Safe, standard software from trusted publishers.<br/>"
            "<font color='orange'><b>Medium</b></font>: Outdated software, or tools requiring caution.<br/>"
            "<font color='red'><b>High</b></font>: Known security risks, malware, or critical vulnerabilities."
        )
        elements.append(Paragraph(legend_text, styles['Normal']))
        elements.append(Spacer(1, 24))

        # Create Table per Category
        for category, progs in grouped_programs.items():
            # Category Header
            cat_header = Paragraph(f"<b>{category}</b> ({len(progs)})", styles['Heading2'])
            elements.append(cat_header)
            elements.append(Spacer(1, 6))

            data = [['Name', 'Version', 'Risk Level', 'Publisher']]
            for prog in progs:
                name = prog.get('name', 'Unknown')[:45]
                version = prog.get('version', 'Unknown')[:15]
                publisher = prog.get('publisher', 'Unknown')[:30]
                security = prog.get('security', 'Unknown')
                data.append([name, version, security, publisher])

            # Table Styling
            table = Table(data, colWidths=[220, 90, 70, 120])
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('ROWBACKGROUNDS', (1, 0), (-1, -1), [colors.whitesmoke, colors.white]),
            ])
            
            # Conditional Formatting for Security
            for i, row in enumerate(data[1:], start=1):
                sec_val = row[2].lower()
                if "high" in sec_val:
                    style.add('TEXTCOLOR', (2, i), (2, i), colors.red)
                    style.add('FONTNAME', (2, i), (2, i), 'Helvetica-Bold')
                elif "medium" in sec_val:
                    style.add('TEXTCOLOR', (2, i), (2, i), colors.orange)
            
            table.setStyle(style)
            elements.append(table)
            elements.append(Spacer(1, 18))

        doc.build(elements)
        print(f"Report generated at {output_path}")
