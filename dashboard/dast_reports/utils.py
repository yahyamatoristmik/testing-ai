import os
import json
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfgen.canvas import Canvas
from datetime import datetime

def add_header(canvas, doc):
    """Add header to every page with date, website info, and logo"""
    canvas.saveState()
    
    # Tambahkan logo OpsiTech di sebelah kiri
    try:
        logo_path = "/home/dj/ai-evaluator/dashboard/staticfiles/opsitech5.jpg"  # Ganti dengan path logo yang benar
        if os.path.exists(logo_path):
            logo = Image(logo_path)
            logo.drawHeight = 1.2*cm
            logo.drawWidth = 1.3*cm
            logo.drawOn(canvas, 2*cm, A4[1] - 1.8*cm)
    except:
        # Fallback jika logo tidak ditemukan
        canvas.setFont('Helvetica-Bold', 12)
        canvas.setFillColor(colors.HexColor('#1a237e'))
        canvas.drawString(2*cm, A4[1] - 1.8*cm, "OpsiTech")
    
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(colors.gray)
    
    # Header text dengan tanggal dan website - dipindah ke kanan
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    header_text = f"{current_date} | opsitech.id Professional Cybersecurity"
    
    # Draw header text - dipindah ke posisi yang lebih ke kanan
    canvas.drawString(10.5*cm, A4[1] - 1.5*cm, header_text)
    
    # Draw header line
    canvas.setStrokeColor(colors.lightgrey)
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, A4[1] - 1.8*cm, A4[0] - 2*cm, A4[1] - 1.8*cm)
    
    canvas.restoreState()

def add_footer(canvas, doc):
    """Add footer to every page"""
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.gray)
    
    # Footer text
    footer_text = "Generated automatically by https://opsitech.id Professional Cybersecurity"
    page_num = f"Page {doc.page}"
    
    # Draw footer text
    canvas.drawString(2*cm, 1*cm, footer_text)
    canvas.drawRightString(A4[0] - 2*cm, 1*cm, page_num)
    
    # Draw footer line
    canvas.setStrokeColor(colors.lightgrey)
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, 1.5*cm, A4[0] - 2*cm, 1.5*cm)
    
    canvas.restoreState()

def generate_scan_pdf(scan, json_data=None):
    """Generate comprehensive PDF report for a single scan with ZAP results"""
    buffer = BytesIO()
    
    # Create document with header and footer
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                          leftMargin=2*cm,
                          rightMargin=2*cm,
                          topMargin=3.5*cm,  # Increased top margin for header with logo
                          bottomMargin=3*cm)
    
    styles = getSampleStyleSheet()
    story = []

    # Cover page dengan logo besar di tengah
    try:
        logo_path = "opsitech5.jpg"
        if os.path.exists(logo_path):
            logo = Image(logo_path)
            logo.drawHeight = 3*cm
            logo.drawWidth = 8*cm
            story.append(Spacer(1, 8*cm))
            story.append(logo)
            
            # Judul perusahaan di bawah logo
            company_style = """
            <para alignment='center'>
            <font name='Helvetica-Bold' size='16' color='#1a237e'>
            OpsiTech
            </font>
            <br/>
            <font name='Helvetica' size='12' color='#455a64'>
            Innovative Solutions
            </font>
            </para>
            """
            story.append(Paragraph(company_style, styles['Normal']))
            story.append(Spacer(1, 2*cm))
    except:
        pass

    # Main Title dengan box biru
    title_style = """
    <para alignment='center'>
    <font name='Helvetica-Bold' size='18' color='#ffffff'>
    DAST SCAN SECURITY REPORT
    </font>
    </para>
    """

    title_table = Table([[Paragraph(title_style, styles['Normal'])]], 
                       colWidths=[16*cm], rowHeights=[1.2*cm])
    title_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1a237e')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#000080')),
    ]))

    story.append(title_table)
    story.append(Spacer(1, 15))

    # Scan Information Header
    scan_info_style = """
    <para alignment='left'>
    <font name='Helvetica-Bold' size='12' color='#d32f2f'>
    ▌ Scan Information
    </font>
    </para>
    """
    story.append(Paragraph(scan_info_style, styles['Normal']))

    # Garis bawah
    line_style = """
    <para alignment='left'>
    <font name='Helvetica' size='1' color='#ffab00'>
    ────────────────────────────────────
    </font>
    </para>
    """
    story.append(Paragraph(line_style, styles['Normal']))
    story.append(Spacer(1, 15))

    scan_info_data = [
        ['Scan Name:', scan.name],
        ['Target URL:', scan.target_url],
        ['Scan Type:', scan.scan_type],
        ['Scan Date:', scan.scan_date.strftime('%Y-%m-%d %H:%M:%S') if scan.scan_date else 'N/A'],
        ['Status:', scan.status],
        ['Owner:', str(scan.owner) if scan.owner else 'N/A'],
        ['Vulnerabilities Found:', str(scan.vulnerabilities_found)]
    ]
    
    scan_info_table = Table(scan_info_data, colWidths=[4*cm, 10*cm])
    story.append(scan_info_table)
    story.append(Spacer(1, 20))
    
    # Vulnerability Summary Header
    vuln_header_style = """
    <para alignment='left'>
    <font name='Helvetica-Bold' size='12' color='#1976d2'>
    ▌ Vulnerability Summary
    </font>
    </para>
    """
    story.append(Paragraph(vuln_header_style, styles['Normal']))
    story.append(Paragraph(line_style, styles['Normal']))
    story.append(Spacer(1, 15))
    
    vuln_summary_data = [
        ['Severity', 'Count'],
        ['High', str(scan.high_vulnerabilities)],
        ['Medium', str(scan.medium_vulnerabilities)],
        ['Low', str(scan.low_vulnerabilities)],
        ['Informational', str(scan.informational_vulnerabilities)],
        ['Total', str(scan.vulnerabilities_found)]
    ]
    
    vuln_summary_table = Table(vuln_summary_data, colWidths=[4*cm, 4*cm])
    vuln_summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#455a64')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(vuln_summary_table)
    story.append(Spacer(1, 20))
    
    # Detailed Vulnerabilities from JSON
    if json_data and 'site' in json_data:
        detailed_header_style = """
        <para alignment='left'>
        <font name='Helvetica-Bold' size='12' color='#f57c00'>
        ▌ Detailed Vulnerability Findings
        </font>
        </para>
        """
        story.append(Paragraph(detailed_header_style, styles['Normal']))
        story.append(Paragraph(line_style, styles['Normal']))
        story.append(Spacer(1, 15))
        
        for site in json_data['site']:
            if 'alerts' in site and site['alerts']:
                for alert in site['alerts']:
                    riskcode = alert.get('riskcode', '0')
                    vuln_name = alert.get('name', 'Unknown')
                    
                    # Vulnerability Header Berwarna
                    if riskcode == '3':
                        vuln_text = f'<font color="#d32f2f"><b>HIGH RISK</b></font>: {vuln_name}'
                    elif riskcode == '2':
                        vuln_text = f'<font color="#f57c00"><b>MEDIUM RISK</b></font>: {vuln_name}'
                    elif riskcode == '1':
                        vuln_text = f'<font color="#ffa000"><b>LOW RISK</b></font>: {vuln_name}'
                    elif riskcode == '0':
                        vuln_text = f'<font color="#1976d2"><b>INFORMATIONAL</b></font>: {vuln_name}'
                    else:
                        vuln_text = f'<font color="#6c757d"><b>UNKNOWN</b></font>: {vuln_name}'
                    
                    story.append(Paragraph(vuln_text, styles['Heading3']))
                    
                    # Description
                    if alert.get('desc'):
                        desc_text = f"<b>Description:</b> {alert.get('desc')}"
                        story.append(Paragraph(desc_text, styles['BodyText']))
                    
                    # Solution
                    if alert.get('solution'):
                        solution_text = f"<b>Solution:</b> {alert.get('solution')}"
                        story.append(Paragraph(solution_text, styles['BodyText']))
                    
                    # Risk
                    if alert.get('riskdesc'):
                        risk_text = f"<b>Risk:</b> {alert.get('riskdesc')}"
                        story.append(Paragraph(risk_text, styles['BodyText']))
                    
                    # Instances - FILTER UNIK UNTUK MENGHINDARI DUPLIKASI
                    if alert.get('instances'):
                        # Mengumpulkan URL unik
                        unique_urls = set()
                        for instance in alert['instances']:
                            url = instance.get('uri', 'Unknown URL')
                            # Hapus parameter query jika ada
                            clean_url = url.split('?')[0] if '?' in url else url
                            unique_urls.add(clean_url)
                        
                        instances_text = f"<b>Affected URLs:</b> {len(alert['instances'])} instances found ({len(unique_urls)} unique URLs)"
                        story.append(Paragraph(instances_text, styles['BodyText']))
                        
                        # Menampilkan URL unik saja
                        for i, url in enumerate(sorted(unique_urls), 1):
                            story.append(Paragraph(f"{i}. {url}", styles['BodyText']))
                    
                    # Additional info
                    if alert.get('otherinfo'):
                        other_text = f"<b>Additional Info:</b> {alert.get('otherinfo')}"
                        story.append(Paragraph(other_text, styles['BodyText']))
                    
                    # References
                    if alert.get('reference'):
                        ref_text = f"<b>References:</b> {alert.get('reference')}"
                        story.append(Paragraph(ref_text, styles['BodyText']))
                    
                    # CWE dan WASC IDs
                    cwe_id = alert.get('cweid', 'Not specified')
                    wasc_id = alert.get('wascid', 'Not specified')
                    if cwe_id != 'Not specified' or wasc_id != 'Not specified':
                        cwe_text = f"<b>Classification:</b> CWE-{cwe_id}, WASC-{wasc_id}"
                        story.append(Paragraph(cwe_text, styles['BodyText']))
                    
                    story.append(Spacer(1, 15))
    
    # Recommendations Header
    recom_header_style = """
    <para alignment='left'>
    <font name='Helvetica-Bold' size='12' color='#388e3c'>
    ▌ Security Recommendations
    </font>
    </para>
    """
    story.append(Paragraph(recom_header_style, styles['Normal']))
    story.append(Paragraph(line_style, styles['Normal']))
    story.append(Spacer(1, 15))
    
    recommendations = [
        "1. Immediately address high-risk vulnerabilities",
        "2. Implement proper input validation",
        "3. Keep all software components updated",
        "4. Implement Web Application Firewall (WAF)",
        "5. Conduct regular security testing",
        "6. Enable proper logging and monitoring"
    ]
    
    for rec in recommendations:
        story.append(Paragraph(rec, styles['BodyText']))
    
    story.append(Spacer(1, 20))
    
    # Build PDF with header and footer
    doc.build(story, onFirstPage=lambda canvas, doc: [add_header(canvas, doc), add_footer(canvas, doc)], 
              onLaterPages=lambda canvas, doc: [add_header(canvas, doc), add_footer(canvas, doc)])
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

# ... (fungsi export_multiple_scans_pdf dan get_risk_level tetap sama)
def export_multiple_scans_pdf(scans):
    """Export multiple scans to a comprehensive PDF report"""
    buffer = BytesIO()
    
    # Create document with header and footer
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                          leftMargin=2*cm,
                          rightMargin=2*cm,
                          topMargin=3*cm,  # Increased top margin for header
                          bottomMargin=3*cm)
    
    styles = getSampleStyleSheet()
    story = []

    # Main Title dengan box merah
    title_style = """
    <para alignment='center'>
    <font name='Helvetica-Bold' size='18' color='#ffffff'>
    MULTIPLE DAST SCAN REPORTS
    </font>
    </para>
    """

    title_table = Table([[Paragraph(title_style, styles['Normal'])]], 
                       colWidths=[16*cm], rowHeights=[1.2*cm])
    title_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#d32f2f')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#b71c1c')),
    ]))

    story.append(title_table)
    story.append(Spacer(1, 20))
    
    # Executive Summary Header
    summary_header_style = """
    <para alignment='left'>
    <font name='Helvetica-Bold' size='12' color='#7b1fa2'>
    ▌ Executive Summary
    </font>
    </para>
    """
    story.append(Paragraph(summary_header_style, styles['Normal']))
    
    line_style = """
    <para alignment='left'>
    <font name='Helvetica' size='1' color='#ffab00'>
    ────────────────────────────────────
    </font>
    </para>
    """
    story.append(Paragraph(line_style, styles['Normal']))
    story.append(Spacer(1, 15))
    
    total_vulns = sum(scan.vulnerabilities_found for scan in scans)
    total_high = sum(scan.high_vulnerabilities for scan in scans)
    
    summary_text = f"""
    This report contains security assessment results for {len(scans)} scans. 
    Total vulnerabilities found: {total_vulns}
    High risk vulnerabilities: {total_high}
    """
    story.append(Paragraph(summary_text, styles['BodyText']))
    story.append(Spacer(1, 20))
    
    # Scan Overview Header
    overview_header_style = """
    <para alignment='left'>
    <font name='Helvetica-Bold' size='12' color='#0288d1'>
    ▌ Scan Overview
    </font>
    </para>
    """
    story.append(Paragraph(overview_header_style, styles['Normal']))
    story.append(Paragraph(line_style, styles['Normal']))
    story.append(Spacer(1, 15))
    
    summary_data = [['Scan Name', 'Target URL', 'Status', 'High', 'Medium', 'Low', 'Total', 'Risk Score']]
    
    for scan in scans:
        summary_data.append([
            scan.name[:20] + '...' if len(scan.name) > 20 else scan.name,
            scan.target_url[:30] + '...' if len(scan.target_url) > 30 else scan.target_url,
            scan.status,
            str(scan.high_vulnerabilities),
            str(scan.medium_vulnerabilities),
            str(scan.low_vulnerabilities),
            str(scan.vulnerabilities_found),
            str(scan.risk_score)
        ])
    
    summary_table = Table(summary_data, colWidths=[3*cm, 4*cm, 2*cm, 1.5*cm, 1.5*cm, 1.5*cm, 1.5*cm, 2*cm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#455a64')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 20))
    
    # Risk Analysis Header
    risk_header_style = """
    <para alignment='left'>
    <font name='Helvetica-Bold' size='12' color='#f57c00'>
    ▌ Risk Analysis
    </font>
    </para>
    """
    story.append(Paragraph(risk_header_style, styles['Normal']))
    story.append(Paragraph(line_style, styles['Normal']))
    story.append(Spacer(1, 15))
    
    risk_data = [
        ['Risk Level', 'Total Count', 'Percentage'],
        ['High', str(total_high), f"{(total_high/total_vulns*100):.1f}%" if total_vulns > 0 else '0%'],
        ['Medium', str(sum(scan.medium_vulnerabilities for scan in scans)), f"{(sum(scan.medium_vulnerabilities for scan in scans)/total_vulns*100):.1f}%" if total_vulns > 0 else '0%'],
        ['Low', str(sum(scan.low_vulnerabilities for scan in scans)), f"{(sum(scan.low_vulnerabilities for scan in scans)/total_vulns*100):.1f}%" if total_vulns > 0 else '0%'],
        ['Total', str(total_vulns), '100%']
    ]
    
    risk_table = Table(risk_data, colWidths=[3*cm, 3*cm, 3*cm])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#455a64')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    story.append(risk_table)
    story.append(Spacer(1, 20))
    
    # Recommendations Header
    recom_header_style = """
    <para alignment='left'>
    <font name='Helvetica-Bold' size='12' color='#388e3c'>
    ▌ Security Recommendations
    </font>
    </para>
    """
    story.append(Paragraph(recom_header_style, styles['Normal']))
    story.append(Paragraph(line_style, styles['Normal']))
    story.append(Spacer(1, 15))
    
    recommendations = [
        "• Prioritize remediation based on risk level",
        "• Implement automated security testing",
        "• Conduct regular penetration testing",
        "• Establish security monitoring",
        "• Provide security training for developers"
    ]
    
    for rec in recommendations:
        story.append(Paragraph(rec, styles['BodyText']))
    
    story.append(Spacer(1, 20))
    
    # Build PDF with header and footer
    doc.build(story, onFirstPage=lambda canvas, doc: [add_header(canvas, doc), add_footer(canvas, doc)], 
              onLaterPages=lambda canvas, doc: [add_header(canvas, doc), add_footer(canvas, doc)])
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

def get_risk_level(riskcode):
    """Convert risk code to human readable level"""
    risk_levels = {
        '3': 'HIGH RISK',
        '2': 'MEDIUM RISK', 
        '1': 'LOW RISK',
        '0': 'INFORMATIONAL'
    }
    return risk_levels.get(riskcode, 'UNKNOWN')
