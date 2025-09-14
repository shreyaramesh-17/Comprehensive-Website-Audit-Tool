from flask import Flask, render_template, redirect, url_for, request, session, send_file
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import requests
import re
import time
from urllib.parse import urlparse
import ssl
import socket
from bs4 import BeautifulSoup
import json
import urllib3
import hashlib
from collections import Counter

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
app.secret_key = "your_secret_key"

def comprehensive_website_audit(url):
    """Comprehensive website audit covering security, performance, SEO, and accessibility"""
    
    # Ensure URL has protocol
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    audit_results = {
        'url': url,
        'scan_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'security': {'score': 0, 'findings': []},
        'performance': {'score': 0, 'findings': []},
        'seo': {'score': 0, 'findings': []},
        'accessibility': {'score': 0, 'findings': []}
    }
    
    try:
        # Basic request with timeout
        start_time = time.time()
        response = requests.get(url, timeout=15, allow_redirects=True, verify=False)
        load_time = time.time() - start_time
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        content = response.text.lower()
        headers = response.headers
        
        # 1. SECURITY AUDIT
        security_score = 100
        security_findings = []
        
        # HTTPS Check
        if not url.startswith('https://'):
            security_score -= 25
            security_findings.append({
                'name': 'HTTPS Not Enabled',
                'description': 'Website is not using secure HTTPS connection',
                'fix_steps': [
                    'Purchase and install SSL certificate',
                    'Configure server to redirect HTTP to HTTPS',
                    'Update all internal links to use HTTPS',
                    'Test all functionality after HTTPS migration'
                ]
            })
        
        # Security Headers
        security_headers = {
            'X-Frame-Options': 'Missing X-Frame-Options header (clickjacking protection)',
            'X-Content-Type-Options': 'Missing X-Content-Type-Options header (MIME sniffing protection)',
            'X-XSS-Protection': 'Missing X-XSS-Protection header (XSS protection)',
            'Strict-Transport-Security': 'Missing HSTS header (HTTPS enforcement)',
            'Content-Security-Policy': 'Missing CSP header (content security policy)',
            'Referrer-Policy': 'Missing Referrer-Policy header (referrer control)'
        }
        
        for header, description in security_headers.items():
            if header not in headers:
                security_score -= 5
                security_findings.append({
                    'name': f'Missing {header}',
                    'description': description,
                    'fix_steps': [
                        f'Add {header} header to server configuration',
                        'Configure appropriate values for the header',
                        'Test the header implementation',
                        'Monitor for any functionality issues'
                    ]
                })
        
        # Server Information Disclosure
        server_headers = ['Server', 'X-Powered-By', 'X-AspNet-Version']
        for header in server_headers:
            if header in headers:
                security_score -= 3
                security_findings.append({
                    'name': f'Server Information Disclosure',
                    'description': f'{header} header reveals server information: {headers[header]}',
                    'fix_steps': [
                        'Remove or modify server information headers',
                        'Configure server to hide version information',
                        'Use generic server names',
                        'Regularly audit server configuration'
                    ]
                })
        
        # SQL Injection Patterns
        sql_patterns = ['mysql_error', 'oracle error', 'sql server error', 'postgresql error']
        for pattern in sql_patterns:
            if pattern in content:
                security_score -= 15
                security_findings.append({
                    'name': 'SQL Error Information Disclosure',
                    'description': f'Database error information is exposed: {pattern}',
                    'fix_steps': [
                        'Implement proper error handling',
                        'Use parameterized queries',
                        'Configure custom error pages',
                        'Enable error logging instead of user display'
                    ]
                })
        
        # XSS Vulnerabilities
        xss_patterns = ['<script>', 'javascript:', 'onerror=', 'onload=']
        for pattern in xss_patterns:
            if pattern in content:
                security_score -= 10
                security_findings.append({
                    'name': 'Potential XSS Vulnerability',
                    'description': f'Potentially dangerous pattern found: {pattern}',
                    'fix_steps': [
                        'Sanitize all user inputs',
                        'Use Content Security Policy (CSP)',
                        'Implement output encoding',
                        'Regular security testing'
                    ]
                })
        
        # 2. PERFORMANCE AUDIT
        performance_score = 100
        performance_findings = []
        
        # Page Load Time
        if load_time > 3:
            performance_score -= 20
            performance_findings.append({
                'name': 'Slow Page Load Time',
                'description': f'Page takes {load_time:.2f} seconds to load (should be under 3 seconds)',
                'fix_steps': [
                    'Optimize server response time',
                    'Minimize HTTP requests',
                    'Enable compression (Gzip)',
                    'Use CDN for static assets',
                    'Optimize images and media files'
                ]
            })
        elif load_time > 1.5:
            performance_score -= 10
            performance_findings.append({
                'name': 'Moderate Page Load Time',
                'description': f'Page takes {load_time:.2f} seconds to load (could be faster)',
                'fix_steps': [
                    'Optimize server configuration',
                    'Reduce server-side processing',
                    'Implement caching strategies',
                    'Optimize database queries'
                ]
            })
        
        # Image Optimization
        images = soup.find_all('img')
        large_images = 0
        for img in images:
            if img.get('width') and img.get('height'):
                width = int(img.get('width'))
                height = int(img.get('height'))
                if width > 1920 or height > 1080:
                    large_images += 1
        
        if large_images > 0:
            performance_score -= 10
            performance_findings.append({
                'name': 'Large Images Detected',
                'description': f'Found {large_images} images that may be too large for web use',
                'fix_steps': [
                    'Resize images to appropriate dimensions',
                    'Use responsive images with srcset',
                    'Implement lazy loading',
                    'Optimize image formats (WebP, AVIF)',
                    'Use image compression tools'
                ]
            })
        
        # JavaScript and CSS Optimization
        scripts = soup.find_all('script')
        stylesheets = soup.find_all('link', rel='stylesheet')
        
        if len(scripts) > 10:
            performance_score -= 5
            performance_findings.append({
                'name': 'Too Many JavaScript Files',
                'description': f'Found {len(scripts)} script tags (consider bundling)',
                'fix_steps': [
                    'Bundle JavaScript files',
                    'Minify JavaScript code',
                    'Use async/defer attributes',
                    'Remove unused JavaScript',
                    'Implement code splitting'
                ]
            })
        
        if len(stylesheets) > 5:
            performance_score -= 5
            performance_findings.append({
                'name': 'Too Many CSS Files',
                'description': f'Found {len(stylesheets)} stylesheet links (consider bundling)',
                'fix_steps': [
                    'Bundle CSS files',
                    'Minify CSS code',
                    'Remove unused CSS',
                    'Use critical CSS inline',
                    'Implement CSS optimization'
                ]
            })
        
        # 3. SEO AUDIT
        seo_score = 100
        seo_findings = []
        
        # Title Tag
        title = soup.find('title')
        if not title or not title.text.strip():
            seo_score -= 20
            seo_findings.append({
                'name': 'Missing Title Tag',
                'description': 'Page has no title tag or empty title',
                'fix_steps': [
                    'Add a unique, descriptive title tag',
                    'Keep title between 50-60 characters',
                    'Include primary keyword naturally',
                    'Make title compelling for users'
                ]
            })
        elif len(title.text) > 60:
            seo_score -= 10
            seo_findings.append({
                'name': 'Title Too Long',
                'description': f'Title is {len(title.text)} characters (should be 50-60)',
                'fix_steps': [
                    'Shorten title to 50-60 characters',
                    'Focus on primary keyword',
                    'Make it compelling and clear',
                    'Test in search results preview'
                ]
            })
        
        # Meta Description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc or not meta_desc.get('content'):
            seo_score -= 15
            seo_findings.append({
                'name': 'Missing Meta Description',
                'description': 'Page has no meta description',
                'fix_steps': [
                    'Add unique meta description',
                    'Keep it between 150-160 characters',
                    'Include primary keyword naturally',
                    'Make it compelling for click-throughs'
                ]
            })
        elif len(meta_desc.get('content', '')) > 160:
            seo_score -= 5
            seo_findings.append({
                'name': 'Meta Description Too Long',
                'description': f'Meta description is {len(meta_desc.get("content", ""))} characters',
                'fix_steps': [
                    'Shorten to 150-160 characters',
                    'Focus on compelling description',
                    'Include primary keyword',
                    'Test in search results'
                ]
            })
        
        # Heading Structure
        h1_tags = soup.find_all('h1')
        if len(h1_tags) == 0:
            seo_score -= 15
            seo_findings.append({
                'name': 'Missing H1 Tag',
                'description': 'Page has no H1 heading tag',
                'fix_steps': [
                    'Add a single H1 tag per page',
                    'Include primary keyword naturally',
                    'Make it descriptive and compelling',
                    'Ensure it matches page content'
                ]
            })
        elif len(h1_tags) > 1:
            seo_score -= 10
            seo_findings.append({
                'name': 'Multiple H1 Tags',
                'description': f'Page has {len(h1_tags)} H1 tags (should have only one)',
                'fix_steps': [
                    'Use only one H1 tag per page',
                    'Convert extra H1s to H2 or H3',
                    'Maintain proper heading hierarchy',
                    'Ensure H1 represents main topic'
                ]
            })
        
        # Alt Text for Images
        images_without_alt = [img for img in images if not img.get('alt')]
        if images_without_alt:
            seo_score -= 10
            seo_findings.append({
                'name': 'Images Missing Alt Text',
                'description': f'{len(images_without_alt)} images missing alt text',
                'fix_steps': [
                    'Add descriptive alt text to all images',
                    'Include relevant keywords naturally',
                    'Describe image content clearly',
                    'Use alt="" for decorative images'
                ]
            })
        
        # 4. ACCESSIBILITY AUDIT
        accessibility_score = 100
        accessibility_findings = []
        
        # Alt Text Check (also affects accessibility)
        if images_without_alt:
            accessibility_score -= 15
            accessibility_findings.append({
                'name': 'Images Missing Alt Text',
                'description': f'{len(images_without_alt)} images missing alt text for screen readers',
                'fix_steps': [
                    'Add descriptive alt text to all images',
                    'Describe image content clearly',
                    'Use alt="" for decorative images',
                    'Test with screen readers'
                ]
            })
        
        # Form Labels
        forms = soup.find_all('form')
        for form in forms:
            inputs = form.find_all('input')
            for input_field in inputs:
                if input_field.get('type') not in ['hidden', 'submit', 'button']:
                    if not input_field.get('id') or not soup.find('label', attrs={'for': input_field.get('id')}):
                        accessibility_score -= 5
                        accessibility_findings.append({
                            'name': 'Form Input Missing Label',
                            'description': 'Form input field missing proper label association',
                            'fix_steps': [
                                'Add unique ID to input field',
                                'Create label with matching "for" attribute',
                                'Use descriptive label text',
                                'Test with screen readers'
                            ]
                        })
                        break
        
        # Color Contrast (basic check)
        if 'color: #' in content or 'background-color: #' in content:
            accessibility_score -= 5
            accessibility_findings.append({
                'name': 'Color Contrast Check Needed',
                'description': 'Page uses custom colors - verify contrast ratios',
                'fix_steps': [
                    'Test color contrast ratios (4.5:1 minimum)',
                    'Use high contrast color combinations',
                    'Test with color blindness simulators',
                    'Provide alternative color schemes'
                ]
            })
        
        # Keyboard Navigation
        if not soup.find('a') and not soup.find('button'):
            accessibility_score -= 10
            accessibility_findings.append({
                'name': 'Keyboard Navigation Issues',
                'description': 'Page may have keyboard navigation problems',
                'fix_steps': [
                    'Ensure all interactive elements are keyboard accessible',
                    'Add skip navigation links',
                    'Test tab order and focus indicators',
                    'Implement proper ARIA labels'
                ]
            })
        
        # Update scores
        audit_results['security']['score'] = max(0, security_score)
        audit_results['security']['findings'] = security_findings
        audit_results['performance']['score'] = max(0, performance_score)
        audit_results['performance']['findings'] = performance_findings
        audit_results['seo']['score'] = max(0, seo_score)
        audit_results['seo']['findings'] = seo_findings
        audit_results['accessibility']['score'] = max(0, accessibility_score)
        audit_results['accessibility']['findings'] = accessibility_findings
        
    except requests.exceptions.RequestException as e:
        audit_results['error'] = f"Failed to access website: {str(e)}"
        audit_results['security']['score'] = 0
        audit_results['performance']['score'] = 0
        audit_results['seo']['score'] = 0
        audit_results['accessibility']['score'] = 0
    
    return audit_results

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enter-url', methods=['GET', 'POST'])
def enter_url():
    if request.method == 'POST':
        website_url = request.form['website_url']
        session['website_url'] = website_url
        return redirect(url_for('scan'))
    return render_template('enter_url.html')

@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/processing')
def processing():
    website_url = session.get('website_url', '')
    if not website_url:
        return redirect(url_for('enter_url'))
    
    # Perform comprehensive audit
    audit_results = comprehensive_website_audit(website_url)
    session['audit_results'] = audit_results
    
    return redirect(url_for('report'))

@app.route('/report')
def report():
    website_url = session.get('website_url', 'Unknown URL')
    audit_results = session.get('audit_results', {})
    
    if not audit_results:
        return redirect(url_for('enter_url'))
    
    return render_template('report_generated.html', 
                         website_url=website_url,
                         audit_results=audit_results)

@app.route('/download-report')
def download_report():
    website_url = session.get('website_url', 'Unknown URL')
    audit_results = session.get('audit_results', {})
    
    if not audit_results:
        return redirect(url_for('enter_url'))
    
    pdf_file = "comprehensive_website_audit_report.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    story.append(Paragraph("Comprehensive Website Audit Report", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("WebAudit.com - Professional Website Analysis", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Meta info
    story.append(Paragraph(f"URL: {website_url}", styles['Normal']))
    story.append(Paragraph(f"Scan Date: {audit_results.get('scan_time', 'Unknown')}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Overall Scores
    story.append(Paragraph("Overall Audit Scores", styles['Heading1']))
    story.append(Spacer(1, 12))
    
    categories = ['security', 'performance', 'seo', 'accessibility']
    category_names = ['Security', 'Performance', 'SEO', 'Accessibility']
    
    for i, category in enumerate(categories):
        score = audit_results.get(category, {}).get('score', 0)
        story.append(Paragraph(f"{category_names[i]}: {score}/100", styles['Heading2']))
        story.append(Spacer(1, 12))
    
    # Detailed Findings
    for category in categories:
        category_name = category_names[categories.index(category)]
        findings = audit_results.get(category, {}).get('findings', [])
        
        if findings:
            story.append(Paragraph(f"{category_name} Findings", styles['Heading1']))
            story.append(Spacer(1, 12))
            
            for finding in findings:
                story.append(Paragraph(finding['name'], styles['Heading3']))
                story.append(Paragraph(finding['description'], styles['Normal']))
                story.append(Paragraph("Steps to Fix:", styles['Heading4']))
                
                for i, step in enumerate(finding['fix_steps'], 1):
                    story.append(Paragraph(f"{i}. {step}", styles['Normal']))
                
                story.append(Spacer(1, 12))
    
    doc.build(story)
    return send_file(pdf_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)