# import tiktoken
# from openai import OpenAI
# from typing import Dict, Any, List
# from ..config import OPENAI_API_KEY
# from ..logger import logger

# client = OpenAI(api_key=OPENAI_API_KEY)

# def count_tokens(text: str) -> int:
#     try:
#         encoding = tiktoken.encoding_for_model("gpt-4")
#         return len(encoding.encode(text))
#     except Exception as e:
#         logger.error(f"Error counting tokens: {e}")
#         return len(text.split())

# def truncate_text(text: str, max_tokens: int = 1000) -> str:
#     if not text:
#         return ""
#     encoding = tiktoken.encoding_for_model("gpt-4")
#     tokens = encoding.encode(text)
#     if len(tokens) > max_tokens:
#         return encoding.decode(tokens[:max_tokens]) + "..."
#     return text

# def analyze_content_issues(content_data: Dict[str, Any]) -> Dict[str, list]:
#     issues = {
#         'title': [],
#         'meta_description': [],
#         'headings': [],
#         'images': [],
#         'content': []
#     }
    
#     if not content_data.get('title'):
#         issues['title'].append('Missing title')
#     elif len(content_data['title']) < 30:
#         issues['title'].append('Title too short')
#     elif len(content_data['title']) > 60:
#         issues['title'].append('Title too long')
        
#     if not content_data.get('meta_description'):
#         issues['meta_description'].append('Missing')
#     elif len(content_data['meta_description']) < 120:
#         issues['meta_description'].append('Too short')
#     elif len(content_data['meta_description']) > 160:
#         issues['meta_description'].append('Too long')
        
#     if not content_data.get('h1_tags'):
#         issues['headings'].append('No H1')
#     elif len(content_data['h1_tags']) > 1:
#         issues['headings'].append('Multiple H1s')
        
#     missing_alt = sum(1 for i in content_data.get('img_alt_texts', []) if not i)
#     if missing_alt:
#         issues['images'].append(f'{missing_alt} missing alts')
        
#     if content_data.get('word_count', 0) < 300:
#         issues['content'].append('Thin content')
        
#     return issues

# def extract_critical_audits(audit_data: dict, max_issues: int = 5) -> dict:
#     critical_issues = {}
#     try:
#         sorted_audits = sorted(
#             [(k, v) for k, v in audit_data.items() if isinstance(v, dict) and v.get('score') is not None],
#             key=lambda x: float(x[1]['score'])
#         )
        
#         for audit_id, audit in sorted_audits[:max_issues]:
#             critical_issues[audit_id] = {
#                 'title': truncate_text(audit.get('title', ''), 100),
#                 'description': truncate_text(audit.get('description', ''), 200)
#             }
#     except Exception as e:
#         logger.error(f"Error extracting audits: {e}")
#     return critical_issues

# def batch_analyze(data: dict, max_batch_tokens: int = 4000) -> List[str]:
#     current_batch = []
#     current_tokens = 0
#     batches = []
    
#     for key, value in data.items():
#         item = f"{key}: {value}"
#         item_tokens = count_tokens(item)
        
#         if current_tokens + item_tokens > max_batch_tokens:
#             if current_batch:
#                 batches.append("\n".join(current_batch))
#             current_batch = [item]
#             current_tokens = item_tokens
#         else:
#             current_batch.append(item)
#             current_tokens += item_tokens
    
#     if current_batch:
#         batches.append("\n".join(current_batch))
    
#     return batches

# def get_recommendations_for_chunk(chunk: dict, url: str) -> str:
#     chunk_type = chunk['type']
#     data = chunk['data']
    
#     base_prompts = {
#         'content': f"Content issues for {url}:",
#         'technical': f"Technical setup for {url}:",
#         'performance': f"Performance data for {url}:"
#     }
    
#     all_recommendations = []
    
#     try:
#         if chunk_type == 'performance':
#             data = {
#                 'score': data.get('performance_score', 0),
#                 'critical_issues': extract_critical_audits(data.get('opportunities', {}))
#             }
        
#         batches = batch_analyze(data)
        
#         for batch in batches:
#             prompt = f"{base_prompts[chunk_type]}\n{batch}\nProvide specific recommendations for these issues."
            
#             if count_tokens(prompt) > 6000:
#                 continue
                
#             response = client.chat.completions.create(
#                 model="gpt-4",
#                 messages=[{"role": "user", "content": prompt}],
#                 max_tokens=1000
#             )
#             all_recommendations.append(response.choices[0].message.content)
        
#         return "\n\n".join(all_recommendations) if all_recommendations else "Error: Data too large to process"
        
#     except Exception as e:
#         logger.error(f"Error getting recommendations for {chunk_type}: {e}")
#         return f"Error analyzing {chunk_type}"

# def generate(url: str, pagespeed_insights: dict, content_data: dict, tech_seo_data: dict) -> dict:
#     try:
#         logger.info(f"Generating recommendations for {url}")
        
#         content_issues = analyze_content_issues(content_data)
        
#         chunks = [
#             {'type': 'content', 'data': content_issues},
#             {'type': 'technical', 'data': tech_seo_data},
#             {'type': 'performance', 'data': pagespeed_insights}
#         ]
        
#         recommendations = {}
#         for chunk in chunks:
#             recommendations[chunk['type']] = get_recommendations_for_chunk(chunk, url)
        
#         return {
#             "content_issues": content_issues,
#             "recommendations": recommendations,
#             "analyzed_url": url
#         }
        
#     except Exception as e:
#         logger.error(f"Error generating recommendations: {e}")
#         raise

# # import tiktoken
# # from openai import OpenAI
# # from typing import Dict, Any, List
# # from config import OPENAI_API_KEY
# # from logger import logger

# # client = OpenAI(api_key=OPENAI_API_KEY)

# # # Previous token counting and truncation functions remain the same
# # def count_tokens(text: str) -> int:
# #     try:
# #         encoding = tiktoken.encoding_for_model("gpt-4")
# #         return len(encoding.encode(text))
# #     except Exception as e:
# #         logger.error(f"Error counting tokens: {e}")
# #         return len(text.split())

# # def truncate_text(text: str, max_tokens: int = 1000) -> str:
# #     if not text:
# #         return ""
# #     encoding = tiktoken.encoding_for_model("gpt-4")
# #     tokens = encoding.encode(text)
# #     if len(tokens) > max_tokens:
# #         return encoding.decode(tokens[:max_tokens]) + "..."
# #     return text

# # def analyze_content_issues(content_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
# #     issues = {}
    
# #     # Title Analysis
# #     title = content_data.get('title', '')
# #     if not title:
# #         issues['title'] = {'issue': 'Missing title', 'current': None}
# #     elif len(title) < 30:
# #         issues['title'] = {'issue': 'Title too short', 'current': title, 'length': len(title)}
# #     elif len(title) > 60:
# #         issues['title'] = {'issue': 'Title too long', 'current': title, 'length': len(title)}
    
# #     # Meta Description Analysis
# #     meta = content_data.get('meta_description')
# #     if not meta:
# #         issues['meta_description'] = {'issue': 'Missing meta description', 'current': None}
# #     elif len(meta) < 120:
# #         issues['meta_description'] = {'issue': 'Meta description too short', 'current': meta, 'length': len(meta)}
# #     elif len(meta) > 160:
# #         issues['meta_description'] = {'issue': 'Meta description too long', 'current': meta, 'length': len(meta)}
    
# #     # Other content analyses remain similar but with more detail
# #     return issues

# # def extract_critical_audits(audit_data: dict, max_issues: int = 10) -> dict:
# #     critical_issues = {}
# #     try:
# #         for audit_id, audit in audit_data.items():
# #             if isinstance(audit, dict) and audit.get('score') is not None:
# #                 score = float(audit.get('score', 1))
# #                 if score < 0.9:  # Include more issues for detailed analysis
# #                     critical_issues[audit_id] = {
# #                         'title': audit.get('title', ''),
# #                         'description': audit.get('description', ''),
# #                         'score': score,
# #                         'wastage': audit.get('numericValue', 0),
# #                         'items': audit.get('details', {}).get('items', [])[:3],  # Top 3 specific items
# #                         'displayValue': audit.get('displayValue', '')
# #                     }
# #     except Exception as e:
# #         logger.error(f"Error extracting audits: {e}")
# #     return critical_issues

# # def create_performance_prompt(performance_data: dict) -> str:
# #     score = performance_data.get('performance_score', 0)
# #     audit_data = extract_critical_audits(performance_data.get('opportunities', {}))
    
# #     audit_details = []
# #     for audit_id, data in audit_data.items():
# #         items_detail = ""
# #         if data['items']:
# #             items_detail = "\nSpecific items:"
# #             for item in data['items']:
# #                 if isinstance(item, dict):
# #                     url = item.get('url', '')
# #                     size = item.get('totalBytes', item.get('wastedBytes', 0))
# #                     if url or size:
# #                         items_detail += f"\n- URL: {url}, Size: {size} bytes"

# #         audit_details.append(f"""
# # Issue: {data['title']}
# # Score: {data['score']}
# # Impact: {data['displayValue']}
# # Description: {data['description']}{items_detail}
# # """)

# #     return f"""Based on PageSpeed Insights data:
# # Overall Performance Score: {score * 100:.1f}/100

# # Detailed Issues and Metrics:
# # {''.join(audit_details)}

# # Provide specific recommendations for each issue:
# # 1. Exact problem description
# # 2. Technical solution with specific steps
# # 3. Expected improvement impact
# # 4. Priority level based on score impact
# # """

# # def get_recommendations_for_chunk(chunk: dict, url: str) -> str:
# #     chunk_type = chunk['type']
# #     data = chunk['data']
    
# #     if chunk_type == 'performance':
# #         prompt = create_performance_prompt(data)
# #     else:
# #         base_prompts = {
# #             'content': f"Content issues:",
# #             'technical': f"Technical setup:"
# #         }
# #         prompt = f"{base_prompts[chunk_type]}\n{data}\nProvide specific recommendations for these issues."
    
# #     try:
# #         response = client.chat.completions.create(
# #             model="gpt-4",
# #             messages=[{
# #                 "role": "system",
# #                 "content": """You are a web performance expert. Analyze the provided PageSpeed Insights data 
# #                 and provide specific, actionable recommendations. Focus on practical solutions and 
# #                 technical steps to implement them. Include code examples or configuration changes 
# #                 where relevant."""
# #             },
# #             {
# #                 "role": "user",
# #                 "content": prompt
# #             }],
# #             max_tokens=1500,
# #             temperature=0.7
# #         )
# #         return response.choices[0].message.content
# #     except Exception as e:
# #         logger.error(f"Error getting recommendations for {chunk_type}: {e}")
# #         return f"Error analyzing {chunk_type}"

# # def generate(url: str, pagespeed_insights: dict, content_data: dict, tech_seo_data: dict) -> dict:
# #     try:
# #         logger.info(f"Generating recommendations for {url}")
        
# #         content_issues = analyze_content_issues(content_data)
        
# #         # Process performance data first and separately
# #         performance_recommendations = get_recommendations_for_chunk(
# #             {'type': 'performance', 'data': pagespeed_insights}, 
# #             url
# #         )
        
# #         # Process other chunks
# #         other_chunks = [
# #             {'type': 'content', 'data': content_issues},
# #             {'type': 'technical', 'data': tech_seo_data}
# #         ]
        
# #         recommendations = {
# #             'performance': performance_recommendations
# #         }
        
# #         for chunk in other_chunks:
# #             recommendations[chunk['type']] = get_recommendations_for_chunk(chunk, url)
        
# #         return {
# #             "content_issues": content_issues,
# #             "performance_data": extract_critical_audits(pagespeed_insights.get('opportunities', {})),
# #             "technical_data": tech_seo_data,
            
# #             "analyzed_url": url,
# #             "recommendations": recommendations
# #         }
        
# #     except Exception as e:
# #         logger.error(f"Error generating recommendations: {e}")
# #         raise

# import tiktoken
# from openai import OpenAI
# from typing import Dict, Any, List
# from config import OPENAI_API_KEY
# from logger import logger

# client = OpenAI(api_key=OPENAI_API_KEY)

# def count_tokens(text: str) -> int:
#     try:
#         encoding = tiktoken.encoding_for_model("gpt-4")
#         return len(encoding.encode(text))
#     except Exception as e:
#         logger.error(f"Error counting tokens: {e}")
#         return len(text.split())

# def truncate_text(text: str, max_tokens: int = 1000) -> str:
#     if not text:
#         return ""
#     encoding = tiktoken.encoding_for_model("gpt-4")
#     tokens = encoding.encode(text)
#     if len(tokens) > max_tokens:
#         return encoding.decode(tokens[:max_tokens]) + "..."
#     return text

# def extract_performance_issues(audit_data: dict) -> dict:
#     """Extract and analyze performance issues from PageSpeed data"""
#     performance_issues = {}
#     try:
#         for audit_id, audit in audit_data.items():
#             if isinstance(audit, dict) and audit.get('score') is not None:
#                 score = float(audit.get('score', 1))
#                 if score < 0.9:
#                     details = audit.get('details', {})
#                     items = details.get('items', [])
                    
#                     affected_resources = []
#                     for item in items[:5]:  # Top 5 problematic resources
#                         resource = {
#                             'url': item.get('url', ''),
#                             'type': item.get('resourceType', ''),
#                             'size': item.get('totalBytes', item.get('wastedBytes', 0)),
#                             'savings_ms': item.get('wastedMs', 0),
#                             'savings_bytes': item.get('wastedBytes', 0)
#                         }
#                         affected_resources.append(resource)
                    
#                     performance_issues[audit_id] = {
#                         'title': audit.get('title', ''),
#                         'score': score,
#                         'impact': audit.get('displayValue', ''),
#                         'description': audit.get('description', ''),
#                         'affected_resources': affected_resources,
#                         'importance': 'high' if score < 0.5 else 'medium'
#                     }
#     except Exception as e:
#         logger.error(f"Error extracting performance issues: {e}")
#     return performance_issues

# def analyze_content_issues(content_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
#     """Analyze content issues with specific locations and fixes"""
#     issues = {}
    
#     # Title Analysis
#     title = content_data.get('title', '')
#     if not title:
#         issues['title'] = {
#             'importance': 'high',
#             'location': '<head> section',
#             'current': None,
#             'problem': 'Missing title tag',
#             'fix': {
#                 'description': 'Add a descriptive title tag',
#                 'code': '<title>Primary Keyword - Secondary Keyword | Brand Name</title>',
#                 'implementation': 'Add the title tag within the <head> section of your HTML'
#             }
#         }
#     elif len(title) < 30:
#         issues['title'] = {
#             'importance': 'medium',
#             'location': f'Current title: "{title}"',
#             'current': {'text': title, 'length': len(title)},
#             'problem': 'Title too short',
#             'fix': {
#                 'description': 'Expand title with relevant keywords',
#                 'suggestion': f'Current ({len(title)} chars) should be 50-60 characters',
#                 'implementation': 'Update the existing title tag with more descriptive content'
#             }
#         }
#     elif len(title) > 60:
#         issues['title'] = {
#             'importance': 'medium',
#             'location': f'Current title: "{title}"',
#             'current': {'text': title, 'length': len(title)},
#             'problem': 'Title too long',
#             'fix': {
#                 'description': 'Shorten title while maintaining keywords',
#                 'suggestion': f'Reduce from {len(title)} to 50-60 characters',
#                 'implementation': 'Edit the title tag to be more concise'
#             }
#         }
        
#     # Meta Description Analysis
#     meta = content_data.get('meta_description')
#     if not meta:
#         issues['meta_description'] = {
#             'importance': 'high',
#             'location': '<head> section',
#             'current': None,
#             'problem': 'Missing meta description',
#             'fix': {
#                 'description': 'Add a compelling meta description',
#                 'code': '<meta name="description" content="Your compelling description here (120-160 characters)">',
#                 'implementation': 'Add the meta description tag within the <head> section'
#             }
#         }
#     elif len(meta) < 120:
#         issues['meta_description'] = {
#             'importance': 'medium',
#             'location': 'Meta description tag',
#             'current': {'text': meta, 'length': len(meta)},
#             'problem': 'Meta description too short',
#             'fix': {
#                 'description': 'Expand meta description',
#                 'suggestion': f'Current ({len(meta)} chars) should be 120-160 characters',
#                 'implementation': 'Enhance the description with more relevant details'
#             }
#         }
    
#     # Heading Analysis
#     h1_tags = content_data.get('h1_tags', [])
#     if not h1_tags:
#         issues['headings'] = {
#             'importance': 'high',
#             'location': 'Page content',
#             'current': None,
#             'problem': 'Missing H1 heading',
#             'fix': {
#                 'description': 'Add a primary H1 heading',
#                 'code': '<h1>Your Primary Page Heading</h1>',
#                 'implementation': 'Add as the main visible heading of your content'
#             }
#         }
#     elif len(h1_tags) > 1:
#         issues['headings'] = {
#             'importance': 'medium',
#             'location': f'Multiple locations: {h1_tags}',
#             'current': h1_tags,
#             'problem': 'Multiple H1 tags',
#             'fix': {
#                 'description': 'Consolidate multiple H1s into one',
#                 'implementation': 'Keep the most important H1 and change others to H2-H6'
#             }
#         }
    
#     return issues

# def analyze_technical_issues(tech_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
#     """Analyze technical issues with specific fixes"""
#     issues = {}
    
#     # HTTPS Check
#     if not tech_data.get('is_https'):
#         issues['https'] = {
#             'importance': 'high',
#             'location': 'Server configuration',
#             'current': 'Using HTTP',
#             'problem': 'Not using HTTPS',
#             'fix': {
#                 'description': 'Implement SSL/HTTPS',
#                 'steps': [
#                     '1. Obtain SSL certificate',
#                     '2. Install on server',
#                     '3. Update server configuration',
#                     '4. Implement redirects'
#                 ],
#                 'code': '''# Apache .htaccess
# RewriteEngine On
# RewriteCond %{HTTPS} off
# RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]'''
#             }
#         }
    
#     # Robots.txt Check
#     if not tech_data.get('has_robots_txt'):
#         issues['robots'] = {
#             'importance': 'medium',
#             'location': 'Root directory (/robots.txt)',
#             'current': 'Missing',
#             'problem': 'No robots.txt file',
#             'fix': {
#                 'description': 'Create robots.txt file',
#                 'code': '''User-agent: *
# Allow: /
# Sitemap: https://yourdomain.com/sitemap.xml''',
#                 'implementation': 'Create robots.txt in the root directory'
#             }
#         }
    
#     # Sitemap Check
#     if not tech_data.get('has_sitemap'):
#         issues['sitemap'] = {
#             'importance': 'medium',
#             'location': 'Root directory (/sitemap.xml)',
#             'current': 'Missing',
#             'problem': 'No XML sitemap',
#             'fix': {
#                 'description': 'Generate and submit XML sitemap',
#                 'steps': [
#                     '1. Generate sitemap using a tool or CMS',
#                     '2. Place in root directory',
#                     '3. Submit to Google Search Console'
#                 ]
#             }
#         }
    
#     return issues

# def format_recommendations(issues: Dict[str, Dict[str, Any]], issue_type: str) -> str:
#     """Format recommendations in a clear, actionable way"""
#     if not issues:
#         return f"No significant {issue_type} issues found."
    
#     formatted = []
#     for issue_id, data in sorted(issues.items(), key=lambda x: x[1].get('importance', 'medium')):
#         priority_marker = "🔴" if data.get('importance') == 'high' else "🟡"
        
#         # Get issue title from either 'problem' or 'title' key
#         issue_title = data.get('problem') or data.get('title', 'Issue found')
#         issue_text = f"{priority_marker} {issue_title}\n"
        
#         # Location information
#         if 'location' in data:
#             issue_text += f"Location: {data['location']}\n"
        
#         # Current state
#         if data.get('current'):
#             current_value = data['current']
#             if isinstance(current_value, dict):
#                 if 'text' in current_value:
#                     issue_text += f"Current: {current_value['text']}\n"
#                 if 'length' in current_value:
#                     issue_text += f"Length: {current_value['length']} characters\n"
#             else:
#                 issue_text += f"Current: {current_value}\n"
        
#         # Handle affected resources for performance issues
#         if 'affected_resources' in data:
#             issue_text += "Affected Resources:\n"
#             for resource in data['affected_resources']:
#                 url = resource.get('url', 'Unknown')
#                 size = resource.get('size', 0)
#                 savings = resource.get('savings_bytes', 0)
#                 issue_text += f"- {url}\n  Size: {size:,} bytes\n  Potential savings: {savings:,} bytes\n"
        
#         # Solution/Fix information
#         if 'fix' in data:
#             issue_text += "Solution:\n"
#             if isinstance(data['fix'], dict):
#                 if 'description' in data['fix']:
#                     issue_text += f"- {data['fix']['description']}\n"
#                 if 'steps' in data['fix']:
#                     issue_text += "Steps:\n" + "\n".join(data['fix']['steps']) + "\n"
#                 if 'code' in data['fix']:
#                     issue_text += f"Example:\n{data['fix']['code']}\n"
#                 if 'implementation' in data['fix']:
#                     issue_text += f"Implementation: {data['fix']['implementation']}\n"
#             else:
#                 issue_text += f"- {data['fix']}\n"
#         elif 'description' in data:  # For performance issues
#             issue_text += f"Description: {data['description']}\n"
#             if 'impact' in data:
#                 issue_text += f"Impact: {data['impact']}\n"
        
#         formatted.append(issue_text)
    
#     return "\n\n".join(formatted)

# def generate(url: str, pagespeed_insights: dict, content_data: dict, tech_seo_data: dict) -> dict:
#     """Generate comprehensive recommendations"""
#     try:
#         logger.info(f"Generating recommendations for {url}")
        
#         # Analyze each aspect
#         performance_issues = extract_performance_issues(pagespeed_insights.get('opportunities', {}))
#         content_issues = analyze_content_issues(content_data)
#         technical_issues = analyze_technical_issues(tech_seo_data)
        
#         # Format recommendations
#         recommendations = {
#             'performance': format_recommendations(performance_issues, 'performance'),
#             'content': format_recommendations(content_issues, 'content'),
#             'technical': format_recommendations(technical_issues, 'technical')
#         }
        
#         return {
#             # 'issues_found': {
#             #     'performance': performance_issues,
#             #     'content': content_issues,
#             #     'technical': technical_issues
#             # },
#             'recommendations': recommendations,
#             # 'analyzed_url': url,
#             'priority_counts': {
#                 'high': sum(1 for issues in [performance_issues, content_issues, technical_issues]
#                            for issue in issues.values() if issue['importance'] == 'high'),
#                 'medium': sum(1 for issues in [performance_issues, content_issues, technical_issues]
#                             for issue in issues.values() if issue['importance'] == 'medium')
#             }
#         }
        
#     except Exception as e:
#         logger.error(f"Error generating recommendations: {e}")
#         raise



import tiktoken
from openai import OpenAI
from typing import Dict, Any, List
from config import OPENAI_API_KEY
from logger import logger

client = OpenAI(api_key=OPENAI_API_KEY)

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

def extract_performance_data(audit_data: dict) -> List[Dict[str, Any]]:
    """Extract and structure performance data for analysis"""
    performance_chunks = []
    try:
        # Group audits by category
        audit_groups = {
            'loading': [],
            'rendering': [],
            'assets': [],
            'other': []
        }
        
        for audit_id, audit in audit_data.items():
            if not isinstance(audit, dict) or audit.get('score') is None:
                continue
                
            score = float(audit.get('score', 1))
            if score >= 0.9:  # Skip high-scoring audits
                continue
                
            audit_info = {
                'id': audit_id,
                'title': audit.get('title', ''),
                'score': score,
                'description': audit.get('description', ''),
                'impact': audit.get('displayValue', ''),
                'resources': []
            }
            
            # Extract resource details
            if 'details' in audit and 'items' in audit['details']:
                for item in audit['details']['items'][:5]:  # Top 5 items
                    resource = {
                        'url': item.get('url', ''),
                        'type': item.get('resourceType', ''),
                        'size': item.get('totalBytes', 0),
                        'wasted': item.get('wastedBytes', 0),
                        'time': item.get('wastedMs', 0)
                    }
                    audit_info['resources'].append(resource)
            
            # Categorize audit
            if any(term in audit_id.lower() for term in ['load', 'time', 'fcp', 'lcp']):
                audit_groups['loading'].append(audit_info)
            elif any(term in audit_id.lower() for term in ['render', 'paint', 'cls']):
                audit_groups['rendering'].append(audit_info)
            elif any(term in audit_id.lower() for term in ['resource', 'asset', 'image', 'script', 'css']):
                audit_groups['assets'].append(audit_info)
            else:
                audit_groups['other'].append(audit_info)
        
        # Create chunks for each group
        for group_name, audits in audit_groups.items():
            if audits:
                performance_chunks.append({
                    'type': group_name,
                    'audits': sorted(audits, key=lambda x: x['score'])
                })
                
    except Exception as e:
        logger.error(f"Error extracting performance data: {e}")
    
    return performance_chunks

def format_performance_chunks(chunks: List[dict]) -> str:
    """Format all performance recommendations with proper structure"""
    formatted_sections = []
    
    for chunk in chunks:
        recommendations = get_performance_recommendations(chunk)
        if recommendations:
            section = f"""=== {chunk['type'].upper()} PERFORMANCE ===

{recommendations}
"""
            formatted_sections.append(section)
    
    return "\n\n".join(formatted_sections)

# def get_performance_recommendations(chunk: dict) -> str:
#     """Get GPT-4 recommendations for a performance chunk"""
#     try:
#         # Prepare audit data for the prompt but in a way that encourages natural response
#         issues_data = []
#         for audit in chunk['audits']:
#             resources = [
#                 f"{res['url']} ({res['size']:,} bytes)"
#                 for res in audit['resources']
#                 if res['url']
#             ]
            
#             issues_data.append({
#                 'title': audit['title'],
#                 'score': audit['score'],
#                 'resources': resources
#             })

#         priority_level = '🔴 High Priority' if any(issue['score'] < 0.5 for issue in issues_data) else '🟡 Medium Priority'

#         prompt = f"""As an SEO and performance expert, I've analyzed the {chunk['type']} aspects of the website.

# For each issue, provide:
# 1. A clear explanation of what's causing performance problems
# 2. Specific technical solutions
# 3. Expected impact after implementation

# Format your response with:
# - Priority markers (🔴 for critical, 🟡 for important)
# - Clear problem statements
# - Step-by-step solutions
# - Code examples where relevant
# - Expected improvements

# Focus on being specific and actionable while maintaining a natural, consultative tone."""

#         response = client.chat.completions.create(
#             model="gpt-4",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": """You are an expert web performance consultant providing recommendations. 
#                     Be conversational yet professional. Don't mention PageSpeed Insights or scores directly. 
#                     Instead, speak as if you've personally analyzed the website and found these issues. 
#                     Each recommendation should start with either 🔴 (for critical issues) or 🟡 (for important but less critical issues)."""
#                 },
#                 {
#                     "role": "assistant",
#                     "content": f"I've analyzed the {chunk['type']} performance of the website. Let me share my findings and recommendations."
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             max_tokens=1500,
#             temperature=0.7
#         )

#         recommendations = response.choices[0].message.content

#         # Add section header with priority level
#         formatted_response = f"{priority_level}\n\n{recommendations}"
        
#         return formatted_response
#     except Exception as e:
#         logger.error(f"Error getting performance recommendations: {e}")
#         return f"Error analyzing {chunk['type']} performance issues"
    
def get_performance_recommendations(chunk: dict) -> str:
    """Get GPT-4 recommendations for a performance chunk"""
    try:
        # Determine priorities based on scores
        critical_scores = sum(1 for audit in chunk['audits'] if audit['score'] < 0.5)
        medium_scores = sum(1 for audit in chunk['audits'] if 0.5 <= audit['score'] < 0.9)
        
        prompt = f"""As a web performance expert analyzing the {chunk['type']} aspects of the website.

For each problem you identify, mark it as:
🔴 for critical issues (severe performance impact)
🟡 for important issues (moderate performance impact)

Structure each problem with:
- Problem description
- Detailed solution
- Expected impact

Focus on being specific and actionable. Write in a natural, consultative tone.
Aim to identify {critical_scores} critical issues and {medium_scores} important issues."""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert web performance consultant. 
                    Mark critical problems with 🔴 and important problems with 🟡.
                    Write in a natural, consultative tone.
                    Focus on specific, actionable recommendations.
                    Each problem should clearly show its priority level."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1500,
            temperature=0.7
        )

        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Error getting performance recommendations: {e}") 
        return f"Error analyzing {chunk['type']} performance issues"

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

def generate(url: str, pagespeed_insights: dict, content_data: dict, tech_seo_data: dict) -> dict:
    """Generate comprehensive recommendations"""
    try:
        logger.info(f"Generating recommendations for {url}")
        
        # Initialize with empty dictionaries if None
        content_issues = analyze_content_issues(content_data or {})
        technical_issues = analyze_technical_issues(tech_seo_data or {})
        
        # Process performance data with GPT-4
        performance_chunks = extract_performance_data(pagespeed_insights.get('opportunities', {}))
        performance_recommendations = []
        
        for chunk in performance_chunks:
            chunk_recommendation = get_performance_recommendations(chunk)
            if chunk_recommendation:
                performance_recommendations.append(f"== {chunk['type'].upper()} PERFORMANCE RECOMMENDATIONS ==\n\n{chunk_recommendation}")
        
        # Prepare recommendations
        recommendations = {
            'performance': "\n\n".join(performance_recommendations) if performance_recommendations else "No significant performance issues found.",
            'content': format_recommendations(content_issues or {}, 'content'),
            'technical': format_recommendations(technical_issues or {}, 'technical')
        }
        
        # Calculate priority counts safely
        high_count = 0
        medium_count = 0
        
        # Count content issues
        if content_issues:
            high_count += sum(1 for issue in content_issues.values() 
                            if issue.get('importance') == 'high')
            medium_count += sum(1 for issue in content_issues.values() 
                              if issue.get('importance') == 'medium')
        
        # Count technical issues
        if technical_issues:
            high_count += sum(1 for issue in technical_issues.values() 
                            if issue.get('importance') == 'high')
            medium_count += sum(1 for issue in technical_issues.values() 
                              if issue.get('importance') == 'medium')
        
        # Count performance issues
        if performance_chunks:
            for chunk in performance_chunks:
                for audit in chunk['audits']:
                    if audit['score'] < 0.5:
                        high_count += 1
                    elif audit['score'] < 0.9:
                        medium_count += 1
        
        return {
            'recommendations': recommendations,
            'priority_counts': {
                'high': high_count,
                'medium': medium_count
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise
