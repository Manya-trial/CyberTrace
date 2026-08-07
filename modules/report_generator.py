from fpdf import FPDF
import base64
import os
from datetime import datetime

class CyberTraceReport(FPDF):
    def header(self):
        self.set_fill_color(13, 20, 39)
        self.rect(0, 0, 210, 30, 'F')
        self.set_font('Arial', 'B', 16)
        self.set_text_color(79, 195, 247)
        self.cell(0, 15, 'CyberTrace - Digital Evidence Report', ln=True, align='C')
        self.set_font('Arial', '', 9)
        self.set_text_color(107, 140, 173)
        self.cell(0, 8, 'Cyber Police Station Jammu | Developed by Manya Gupta', ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(107, 140, 173)
        self.cell(0, 10, f'Page {self.page_no()} | CyberTrace | Confidential', align='C')

def generate_report(module_name, data, chart_b64=None):
    try:
        pdf = CyberTraceReport()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Title
        pdf.set_font('Arial', 'B', 13)
        pdf.set_text_color(30, 30, 60)
        pdf.set_fill_color(220, 235, 250)
        pdf.cell(0, 10, f'Module: {module_name}', ln=True, fill=True)
        pdf.ln(3)

        # Timestamp
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 8, f'Report Generated: {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}', ln=True)
        pdf.cell(0, 8, f'Analyst: Manya Gupta | Cyber Police Station Jammu', ln=True)
        pdf.ln(5)

        # Divider
        pdf.set_draw_color(79, 195, 247)
        pdf.set_line_width(0.5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)

        # Data rows
        pdf.set_font('Arial', 'B', 11)
        pdf.set_text_color(20, 60, 120)
        pdf.cell(0, 8, 'Findings:', ln=True)
        pdf.ln(2)

        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(30, 30, 30)

        for key, value in data.items():
            if key in ['status', 'chart_callers', 'chart_network', 'received_ips', 'top_callers']:
                continue
            if isinstance(value, bool):
                value = 'Yes' if value else 'No'
            pdf.set_font('Arial', 'B', 10)
            pdf.set_text_color(20, 60, 120)
            pdf.cell(55, 8, str(key).replace('_', ' ').title() + ':', border=0)
            pdf.set_font('Arial', '', 10)
            pdf.set_text_color(30, 30, 30)
            pdf.multi_cell(0, 8, str(value), border=0)

        # Received IPs (email module)
        if 'received_ips' in data and data['received_ips']:
            pdf.ln(3)
            pdf.set_font('Arial', 'B', 11)
            pdf.set_text_color(20, 60, 120)
            pdf.cell(0, 8, 'Traced IPs:', ln=True)
            for ip in data['received_ips']:
                pdf.set_font('Arial', '', 10)
                pdf.set_text_color(30, 30, 30)
                pdf.cell(0, 7, f"  IP: {ip['ip']} | {ip['city']}, {ip['country']} | ISP: {ip['isp']}", ln=True)

        # Chart image
        if chart_b64:
            pdf.ln(5)
            pdf.set_font('Arial', 'B', 11)
            pdf.set_text_color(20, 60, 120)
            pdf.cell(0, 8, 'Visual Analysis:', ln=True)
            img_data = base64.b64decode(chart_b64)
            tmp_path = 'tmp_chart.png'
            with open(tmp_path, 'wb') as f:
                f.write(img_data)
            pdf.image(tmp_path, w=180)
            os.remove(tmp_path)

        # Save
        filename = f"CyberTrace_{module_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        import io
        buffer = io.BytesIO()
        pdf.output(buffer)
        buffer.seek(0)
        return buffer.getvalue()

    except Exception as e:
        return None