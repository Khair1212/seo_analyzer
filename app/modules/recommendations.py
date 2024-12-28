import tiktoken
from openai import OpenAI
from typing import Dict, Any, List, Optional
from ..config import OPENAI_API_KEY
from ..logger import logger

client = OpenAI(api_key=OPENAI_API_KEY)

# Keep your existing utility functions
def count_tokens(text: str) -> int:
    try:
        encoding = tiktoken.encoding_for_model("gpt-4")
        return len(encoding.encode(text))
    except Exception as e:
        logger.error(f"Error counting tokens: {e}")
        return len(text.split())

def truncate_text(text: str, max_tokens: int = 1000) -> str:
    if not text:
        return ""
    encoding = tiktoken.encoding_for_model("gpt-4")
    tokens = encoding.encode(text)
    if len(tokens) > max_tokens:
        return encoding.decode(tokens[:max_tokens]) + "..."
    return text

# Add new class for enhanced issue tracking
class PerformanceIssue:
    def __init__(self, 
                 issue_type: str,
                 title: str,
                 score: float,
                 description: str,
                 impact: Dict[str, Any],
                 location: Optional[Dict[str, Any]] = None,
                 resources: List[Dict[str, Any]] = None):
        self.issue_type = issue_type
        self.title = title
        self.score = score
        self.description = description
        self.impact = impact
        self.location = location or {}
        self.resources = resources or []
        
    def get_severity(self) -> str:
        if self.score < 0.5:
            return 'critical'
        elif self.score < 0.9:
            return 'warning'
        return 'info'
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.issue_type,
            'title': self.title,
            'severity': self.get_severity(),
            'score': self.score,
            'description': self.description,
            'location': self.location,
            'impact': self.impact,
            'resources': self.resources
        }

# Keep and enhance your location extraction function
def extract_resource_location(item: dict) -> dict:
    """Extract specific location information from a resource"""
    location = {
        'file': '',
        'line': None,
        'column': None,
        'selector': '',
        'context': '',
        'url': item.get('url', '')  # Add URL to location info
    }
    
    # Extract source location
    if 'source' in item:
        location.update({
            'file': item['source'].get('file', ''),
            'line': item['source'].get('line', None),
            'column': item['source'].get('column', None)
        })
    
    # Extract DOM location for elements
    if 'node' in item:
        node = item['node']
        location.update({
            'selector': node.get('selector', ''),
            'context': node.get('snippet', ''),
            'nodeLabel': node.get('nodeLabel', ''),
            'path': node.get('path', ''),
            'boundingRect': node.get('boundingRect', {})
        })
        
    return location

# Keep your format functions with minor enhancements
def format_location(location: dict) -> str:
    """Format location information for display"""
    parts = []
    
    if location['file']:
        parts.append(f"File: {location['file']}")
        if location['line']:
            parts.append(f"Line: {location['line']}")
        if location['column']:
            parts.append(f"Column: {location['column']}")
    
    if location['selector']:
        parts.append(f"DOM: {location['selector']}")
        if location.get('nodeLabel'):
            parts.append(f"Element: {location['nodeLabel']}")
    
    if location.get('url'):
        parts.append(f"URL: {location['url']}")
        
    return ', '.join(parts) if parts else "Location not available"

def format_size(bytes: int) -> str:
    """Format byte sizes in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.1f}{unit}"
        bytes /= 1024
    return f"{bytes:.1f}TB"

# Enhance your extract_performance_data function
def extract_performance_data(pagespeed_data: dict) -> dict:
    """Extract and categorize performance data with enhanced issue tracking"""
    results = {
        'opportunities': [],
        'diagnostics': [],
        'metrics': []
    }
    
    try:
        # Define audit categories with patterns
        categories = {
            'loading': ['largest-contentful-paint', 'first-contentful-paint', 'speed-index'],
            'interactivity': ['interactive', 'blocking-time', 'cpu-time'],
            'visual_stability': ['cumulative-layout-shift', 'layout-shift-elements'],
            'resources': ['render-blocking-resources', 'unused-javascript', 'unused-css'],
            'images': ['modern-image-formats', 'sized-images', 'responsive-images'],
            'caching': ['uses-long-cache-ttl', 'efficient-cache-policy']
        }
        
        for audit_id, audit in pagespeed_data.items():
            if not isinstance(audit, dict) or audit.get('score') is None:
                continue
                
            score = float(audit.get('score', 1))
            if score >= 0.9:  # Skip high-scoring audits
                continue
            
            # Create enhanced issue object
            issue = PerformanceIssue(
                issue_type=determine_category(audit_id, categories),
                title=audit.get('title', ''),
                score=score,
                description=audit.get('description', ''),
                impact={
                    'displayValue': audit.get('displayValue', ''),
                    'numericValue': audit.get('numericValue'),
                    'numericUnit': audit.get('numericUnit', '')
                }
            )
            
            # Extract resource details with enhanced location tracking
            if 'details' in audit and 'items' in audit['details']:
                for item in audit['details']['items'][:5]:  # Limit to top 5 items
                    resource = {
                        'url': item.get('url', ''),
                        'type': item.get('resourceType', ''),
                        'size': item.get('totalBytes', 0),
                        'wasted': item.get('wastedBytes', 0),
                        'time': item.get('wastedMs', 0),
                        'location': extract_resource_location(item)
                    }
                    issue.resources.append(resource)
            
            # Add to appropriate category
            if audit.get('details', {}).get('type') == 'opportunity':
                results['opportunities'].append(issue)
            else:
                results['diagnostics'].append(issue)
                
    except Exception as e:
        logger.error(f"Error extracting performance data: {e}")
        
    return results

def determine_category(audit_id: str, categories: Dict[str, List[str]]) -> str:
    """Determine the category of a performance issue"""
    audit_id_lower = audit_id.lower()
    for category, patterns in categories.items():
        if any(pattern in audit_id_lower for pattern in patterns):
            return category
    return 'other'

# Enhance your get_performance_recommendations function
def get_performance_recommendations(issue: PerformanceIssue) -> str:
    """Generate detailed recommendations for a performance issue"""
    try:
        # Prepare detailed resource analysis
        resource_analysis = []
        for resource in issue.resources:
            location = format_location(resource['location'])
            
            # Extract DOM details if available
            dom_details = ""
            if resource['location'].get('selector'):
                dom_details = f"""
DOM Location:
- Selector: {resource['location']['selector']}
- Element: {resource['location'].get('nodeLabel', 'Not specified')}
- HTML Context: {resource['location'].get('context', 'Not available')}"""

            # Extract file details if available
            file_details = ""
            if resource['location'].get('file'):
                file_details = f"""
File Location:
- Path: {resource['location']['file']}
- Line: {resource['location'].get('line', 'Not specified')}
- Column: {resource['location'].get('column', 'Not specified')}"""

            # Format resource analysis with detailed breakdown
            analysis = f"""
Resource Details:
URL: {resource['url']}
Type: {resource.get('type', 'Not specified')}
Current Size: {format_size(resource['size'])}
Potential Savings: {format_size(resource['wasted'])}
Time Impact: {resource['time']}ms
{dom_details}
{file_details}
Current Implementation Issues:
- Size: {format_size(resource['size'])} (Can be optimized to save {format_size(resource['wasted'])})
- Loading Time: {resource['time']}ms impact on page load"""
            resource_analysis.append(analysis)
        
        prompt = f"""Analyze this {issue.issue_type} performance issue and provide specific solutions. Always start with the specific problematic resources and their locations:

ISSUE: {issue.title}
Severity: {issue.get_severity().upper()}
Score: {issue.score}
Impact: {issue.impact['displayValue']}

AFFECTED RESOURCES AND LOCATIONS:
{chr(10).join(resource_analysis) if resource_analysis else 'No specific resources identified'}

Description:
{issue.description}

Provide:
1. SPECIFIC PROBLEMS BY RESOURCE
- List each problematic resource
- Current implementation issues for each
- Technical impact of each issue

2. DETAILED SOLUTION FOR EACH RESOURCE
- Specific changes needed for each file/resource
- Exact code or configuration changes with examples
- Step-by-step implementation guide per resource
- Required tools and commands with examples

3. VERIFICATION STEPS
- How to verify the fix
- Expected improvements
- Tools to measure impact"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert web performance consultant.
                    Provide detailed, actionable solutions with:
                    1. Specific file locations and code examples
                    2. Step-by-step implementation guides
                    3. Expected improvements with metrics"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=2000,
            temperature=0.7
        )

        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        return f"Error analyzing {issue.issue_type} performance issue"
    

def analyze_content_issues(content_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Analyze content issues with specific locations and fixes"""
    issues = {}
    
    # Title Analysis
    title = content_data.get('title', '')
    if not title:
        issues['title'] = {
            'importance': 'high',
            'location': '<head> section',
            'current': None,
            'problem': 'Missing title tag',
            'fix': {
                'description': 'Add a descriptive title tag',
                'code': '<title>Primary Keyword - Secondary Keyword | Brand Name</title>',
                'implementation': 'Add the title tag within the <head> section of your HTML'
            }
        }
    elif len(title) < 30:
        issues['title'] = {
            'importance': 'medium',
            'location': f'Current title: "{title}"',
            'current': {'text': title, 'length': len(title)},
            'problem': 'Title too short',
            'fix': {
                'description': 'Expand title with relevant keywords',
                'suggestion': f'Current ({len(title)} chars) should be 50-60 characters',
                'implementation': 'Update the existing title tag with more descriptive content'
            }
        }
    elif len(title) > 60:
        issues['title'] = {
            'importance': 'medium',
            'location': f'Current title: "{title}"',
            'current': {'text': title, 'length': len(title)},
            'problem': 'Title too long',
            'fix': {
                'description': 'Shorten title while maintaining keywords',
                'suggestion': f'Reduce from {len(title)} to 50-60 characters',
                'implementation': 'Edit the title tag to be more concise'
            }
        }
        
    # Meta Description Analysis
    meta = content_data.get('meta_description')
    if not meta:
        issues['meta_description'] = {
            'importance': 'high',
            'location': '<head> section',
            'current': None,
            'problem': 'Missing meta description',
            'fix': {
                'description': 'Add a compelling meta description',
                'code': '<meta name="description" content="Your compelling description here (120-160 characters)">',
                'implementation': 'Add the meta description tag within the <head> section'
            }
        }
    elif len(meta) < 120:
        issues['meta_description'] = {
            'importance': 'medium',
            'location': 'Meta description tag',
            'current': {'text': meta, 'length': len(meta)},
            'problem': 'Meta description too short',
            'fix': {
                'description': 'Expand meta description',
                'suggestion': f'Current ({len(meta)} chars) should be 120-160 characters',
                'implementation': 'Enhance the description with more relevant details'
            }
        }
    
    # Heading Analysis
    h1_tags = content_data.get('h1_tags', [])
    if not h1_tags:
        issues['headings'] = {
            'importance': 'high',
            'location': 'Page content',
            'current': None,
            'problem': 'Missing H1 heading',
            'fix': {
                'description': 'Add a primary H1 heading',
                'code': '<h1>Your Primary Page Heading</h1>',
                'implementation': 'Add as the main visible heading of your content'
            }
        }
    elif len(h1_tags) > 1:
        issues['headings'] = {
            'importance': 'medium',
            'location': f'Multiple locations: {h1_tags}',
            'current': h1_tags,
            'problem': 'Multiple H1 tags',
            'fix': {
                'description': 'Consolidate multiple H1s into one',
                'implementation': 'Keep the most important H1 and change others to H2-H6'
            }
        }
    
    return issues

def analyze_technical_issues(tech_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Analyze technical issues with specific fixes"""
    issues = {}
    
    # HTTPS Check
    if not tech_data.get('is_https'):
        issues['https'] = {
            'importance': 'high',
            'location': 'Server configuration',
            'current': 'Using HTTP',
            'problem': 'Not using HTTPS',
            'fix': {
                'description': 'Implement SSL/HTTPS',
                'steps': [
                    '1. Obtain SSL certificate',
                    '2. Install on server',
                    '3. Update server configuration',
                    '4. Implement redirects'
                ],
                'code': '''# Apache .htaccess
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]'''
            }
        }
    
    # Robots.txt Check
    if not tech_data.get('has_robots_txt'):
        issues['robots'] = {
            'importance': 'medium',
            'location': 'Root directory (/robots.txt)',
            'current': 'Missing',
            'problem': 'No robots.txt file',
            'fix': {
                'description': 'Create robots.txt file',
                'code': '''User-agent: *
Allow: /
Sitemap: https://yourdomain.com/sitemap.xml''',
                'implementation': 'Create robots.txt in the root directory'
            }
        }
    
    # Sitemap Check
    if not tech_data.get('has_sitemap'):
        issues['sitemap'] = {
            'importance': 'medium',
            'location': 'Root directory (/sitemap.xml)',
            'current': 'Missing',
            'problem': 'No XML sitemap',
            'fix': {
                'description': 'Generate and submit XML sitemap',
                'steps': [
                    '1. Generate sitemap using a tool or CMS',
                    '2. Place in root directory',
                    '3. Submit to Google Search Console'
                ]
            }
        }
    
    return issues

def format_recommendations(issues: Dict[str, Dict[str, Any]], issue_type: str) -> str:
    """Format recommendations in a clear, actionable way"""
    if not issues:
        return f"No significant {issue_type} issues found."
    
    formatted = []
    for issue_id, data in sorted(issues.items(), key=lambda x: x[1].get('importance', 'medium')):
        priority_marker = "🔴" if data.get('importance') == 'high' else "🟡"
        
        # Get issue title from either 'problem' or 'title' key
        issue_title = data.get('problem') or data.get('title', 'Issue found')
        issue_text = f"{priority_marker} {issue_title}\n"
        
        # Location information
        if 'location' in data:
            issue_text += f"Location: {data['location']}\n"
        
        # Current state
        if data.get('current'):
            current_value = data['current']
            if isinstance(current_value, dict):
                if 'text' in current_value:
                    issue_text += f"Current: {current_value['text']}\n"
                if 'length' in current_value:
                    issue_text += f"Length: {current_value['length']} characters\n"
            else:
                issue_text += f"Current: {current_value}\n"
        
        # Handle affected resources for performance issues
        if 'affected_resources' in data:
            issue_text += "Affected Resources:\n"
            for resource in data['affected_resources']:
                url = resource.get('url', 'Unknown')
                size = resource.get('size', 0)
                savings = resource.get('savings_bytes', 0)
                issue_text += f"- {url}\n  Size: {size:,} bytes\n  Potential savings: {savings:,} bytes\n"
        
        # Solution/Fix information
        if 'fix' in data:
            issue_text += "Solution:\n"
            if isinstance(data['fix'], dict):
                if 'description' in data['fix']:
                    issue_text += f"- {data['fix']['description']}\n"
                if 'steps' in data['fix']:
                    issue_text += "Steps:\n" + "\n".join(data['fix']['steps']) + "\n"
                if 'code' in data['fix']:
                    issue_text += f"Example:\n{data['fix']['code']}\n"
                if 'implementation' in data['fix']:
                    issue_text += f"Implementation: {data['fix']['implementation']}\n"
            else:
                issue_text += f"- {data['fix']}\n"
        elif 'description' in data:  # For performance issues
            issue_text += f"Description: {data['description']}\n"
            if 'impact' in data:
                issue_text += f"Impact: {data['impact']}\n"
        
        formatted.append(issue_text)
    
    return "\n\n".join(formatted)


# Keep your generate function with enhanced integration
def generate(url: str, pagespeed_insights: dict, content_data: dict, tech_seo_data: dict) -> dict:
    """Generate comprehensive recommendations"""
    try:
        logger.info(f"Generating recommendations for {url}")
        
        # Extract performance data with enhanced tracking
        performance_data = extract_performance_data(pagespeed_insights.get('opportunities', {}))
        
        # Generate recommendations for each issue
        performance_recommendations = []
        for issue in performance_data['opportunities'] + performance_data['diagnostics']:
            recommendation = get_performance_recommendations(issue)
            if recommendation:
                severity_marker = '🔴' if issue.get_severity() == 'critical' else '🟡'
                performance_recommendations.append(
                    f"{severity_marker} {issue.title}\n{recommendation}"
                )
        
        # Keep your existing content and technical analysis
        content_issues = analyze_content_issues(content_data or {})
        technical_issues = analyze_technical_issues(tech_seo_data or {})
        
        # Prepare complete recommendations
        return {
            'recommendations': {
                'performance': "\n\n".join(performance_recommendations),
                'content': format_recommendations(content_issues, 'content'),
                'technical': format_recommendations(technical_issues, 'technical')
            },
            'priority_counts': calculate_priority_counts(
                performance_data, content_issues, technical_issues
            )
        }
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise

def calculate_priority_counts(
    performance_data: dict,
    content_issues: Dict[str, Dict[str, Any]],
    technical_issues: Dict[str, Dict[str, Any]]
) -> Dict[str, int]:
    """Calculate priority counts across all issue types"""
    high_count = 0
    medium_count = 0
    
    # Count performance issues
    for issue in performance_data['opportunities'] + performance_data['diagnostics']:
        if issue.score < 0.5:
            high_count += 1
        elif issue.score < 0.9:
            medium_count += 1
    
    # Count content and technical issues
    for issues in [content_issues, technical_issues]:
        if issues:
            high_count += sum(1 for issue in issues.values() 
                            if issue.get('importance') == 'high')
            medium_count += sum(1 for issue in issues.values() 
                              if issue.get('importance') == 'medium')
    
    return {
        'high': high_count,
        'medium': medium_count
    }


