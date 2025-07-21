import json
import os
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from config import Config

class ChatBasedGenerator:
    """Generator class for creating synthetic chat conversations and emails"""
    
    def __init__(self):
        """Initialize the generator"""
        self.domain_prompts = Config.DOMAIN_PROMPTS
        self.available_domains = list(self.domain_prompts.keys())
    
    def get_available_domains(self) -> List[str]:
        """Get list of available domains for chat generation"""
        return self.available_domains
    
    def generate_chat_conversation(self, domain: str, topic: str = None, 
                                 num_turns: int = 5) -> Dict[str, Any]:
        """Generate synthetic chat conversation using template-based approach"""
        try:
            print(f"Generating chat conversation for domain: {domain}, topic: {topic}, turns: {num_turns}")
            
            # Use template-based generation instead of API calls
            conversation = self._generate_conversation_template(domain, topic, num_turns)
            
            print(f"Generated conversation with {len(conversation['messages'])} messages")
            return conversation
            
        except Exception as e:
            print(f"Error in generate_chat_conversation: {str(e)}")
            raise Exception(f"Error generating chat conversation: {str(e)}")
    
    def generate_email(self, domain: str, topic: str = None, 
                      email_type: str = "business") -> Dict[str, Any]:
        """Generate synthetic email using template-based approach"""
        try:
            print(f"Generating email for domain: {domain}, topic: {topic}, type: {email_type}")
            
            # Use template-based generation instead of API calls
            email = self._generate_email_template(domain, topic, email_type)
            
            print(f"Generated email successfully")
            return email
            
        except Exception as e:
            print(f"Error in generate_email: {str(e)}")
            raise Exception(f"Error generating email: {str(e)}")
    
    def _generate_conversation_template(self, domain: str, topic: str, num_turns: int) -> Dict[str, Any]:
        """Generate conversation using predefined templates"""
        
        # Template conversations for different domains
        templates = {
            'customer_support': [
                {"role": "customer", "message": "Hi, I'm having trouble with my order #12345"},
                {"role": "agent", "message": "Hello! I'd be happy to help you with your order. Can you provide more details about the issue?"},
                {"role": "customer", "message": "I ordered a laptop but received a different model than what I ordered"},
                {"role": "agent", "message": "I apologize for the inconvenience. Let me check your order details and help you resolve this."},
                {"role": "customer", "message": "Thank you, I appreciate your help"},
                {"role": "agent", "message": "You're welcome! I'll process a replacement order for you right away."}
            ],
            'chatbot_training': [
                {"role": "user", "message": "What's the weather like today?"},
                {"role": "bot", "message": "I can help you check the weather. What city are you in?"},
                {"role": "user", "message": "I'm in New York"},
                {"role": "bot", "message": "The weather in New York is currently 72°F with partly cloudy skies."},
                {"role": "user", "message": "Will it rain later?"},
                {"role": "bot", "message": "There's a 30% chance of rain this afternoon in New York."}
            ],
            'spam_detection': [
                {"role": "sender", "message": "URGENT: You've won $1,000,000! Click here to claim now!"},
                {"role": "recipient", "message": "This looks like spam"},
                {"role": "sender", "message": "Limited time offer! Don't miss out on this amazing opportunity!"},
                {"role": "recipient", "message": "I'm not interested, please stop contacting me"},
                {"role": "sender", "message": "Last chance! Claim your prize before it expires!"},
                {"role": "recipient", "message": "This is definitely spam, I'm blocking this sender"}
            ],
            'business_communication': [
                {"role": "sender", "message": "Hi John, I wanted to discuss the Q4 project timeline"},
                {"role": "recipient", "message": "Hi Sarah, sure! What specific aspects would you like to review?"},
                {"role": "sender", "message": "I'm concerned about meeting the December deadline"},
                {"role": "recipient", "message": "I understand your concern. Let's schedule a meeting to review the current progress"},
                {"role": "sender", "message": "That would be great. How about tomorrow at 2 PM?"},
                {"role": "recipient", "message": "Perfect! I'll send you a calendar invite for tomorrow at 2 PM"}
            ]
        }
        
        # Get base template for domain
        base_template = templates.get(domain, templates['customer_support'])
        
        # Generate conversation based on template
        conversation = {
            "conversation_id": f"conv_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "domain": domain,
            "topic": topic or "general",
            "num_turns": num_turns,
            "messages": [],
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "model_type": "template",
                "language": "en"
            }
        }
        
        # Generate messages based on template
        for i in range(min(num_turns, len(base_template))):
            message = base_template[i].copy()
            message["timestamp"] = (datetime.now() - timedelta(minutes=num_turns-i)).isoformat()
            message["turn"] = i + 1
            conversation["messages"].append(message)
        
        return conversation
    
    def _generate_email_template(self, domain: str, topic: str, email_type: str) -> Dict[str, Any]:
        """Generate email using predefined templates"""
        
        # Template emails for different domains
        templates = {
            'spam_detection': {
                'subject': 'URGENT: You\'ve won $1,000,000!',
                'from': 'winner@lottery.com',
                'to': 'user@example.com',
                'body': 'Congratulations! You have been selected to receive $1,000,000. Click here to claim your prize now! Limited time offer!'
            },
            'business_communication': {
                'subject': 'Q4 Project Update',
                'from': 'sarah.manager@company.com',
                'to': 'john.employee@company.com',
                'body': 'Hi John,\n\nI wanted to discuss the Q4 project timeline and address some concerns about meeting our December deadline.\n\nBest regards,\nSarah'
            }
        }
        
        # Get base template for domain
        base_template = templates.get(domain, templates['business_communication'])
        
        # Generate email based on template
        email = {
            "email_id": f"email_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "domain": domain,
            "topic": topic or "general",
            "email_type": email_type,
            "subject": base_template['subject'],
            "from": base_template['from'],
            "to": base_template['to'],
            "body": base_template['body'],
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "model_type": "template",
                "language": "en"
            }
        }
        
        return email
    
    def save_to_file(self, data: List[Dict[str, Any]], filename: str, 
                    format: str = "json", user_id: str = None) -> str:
        """Save generated data to file"""
        try:
            print(f"Saving {len(data)} chat records to file with format: {format}")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename}_{timestamp}.{format}"
            
            if user_id:
                user_dir = Config.CHATBASED_DATA_DIR / user_id
                user_dir.mkdir(exist_ok=True, parents=True)
                filepath = user_dir / filename
            else:
                filepath = Config.CHATBASED_DATA_DIR / filename
            
            print(f"File will be saved to: {filepath}")
            
            if format == "json":
                print("Saving as JSON...")
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            elif format == "csv":
                print("Saving as CSV...")
                # Convert to CSV format
                import pandas as pd
                flattened_data = []
                for item in data:
                    if 'messages' in item:  # Chat conversation
                        for msg in item['messages']:
                            flattened_data.append({
                                'conversation_id': item.get('conversation_id', ''),
                                'domain': item.get('domain', ''),
                                'role': msg.get('role', ''),
                                'message': msg.get('message', ''),
                                'timestamp': msg.get('timestamp', ''),
                                'turn': msg.get('turn', '')
                            })
                    else:  # Email
                        flattened_data.append(item)
                
                df = pd.DataFrame(flattened_data)
                df.to_csv(filepath, index=False, encoding='utf-8')
            else:
                raise ValueError("Format must be 'json' or 'csv'")
            
            print(f"File saved successfully to: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"Error in save_to_file: {str(e)}")
            raise e 