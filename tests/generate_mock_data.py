#!/usr/bin/env python3
"""
Mock Data Generator for Employee Onboarding Assistant

This script generates realistic mock data for testing the onboarding assistant system.
It creates comprehensive datasets for:
- Member information (team members, roles, contacts)
- Process information (workflows, procedures, policies)
- Tech stack information (technologies, tools, frameworks)
- Chat history (conversation examples)
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
import os
from pathlib import Path

class MockDataGenerator:
    """Generator for creating realistic mock data for the onboarding system."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize the generator with data directory path."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Sample data pools for realistic generation
        self.departments = [
            "Engineering", "Product", "Design", "Marketing", "Sales", 
            "HR", "Finance", "Operations", "Data Science", "DevOps"
        ]
        
        self.roles = {
            "Engineering": [
                "Senior Software Engineer", "Software Engineer", "Junior Software Engineer",
                "Tech Lead", "Principal Engineer", "Engineering Manager", "DevOps Engineer",
                "Frontend Developer", "Backend Developer", "Full Stack Developer",
                "Mobile Developer", "QA Engineer", "Site Reliability Engineer"
            ],
            "Product": [
                "Product Manager", "Senior Product Manager", "Product Owner",
                "Product Analyst", "Product Designer", "UX Researcher"
            ],
            "Design": [
                "UX Designer", "UI Designer", "Product Designer", "Design Lead",
                "Visual Designer", "Design System Engineer"
            ],
            "Data Science": [
                "Data Scientist", "Senior Data Scientist", "Data Engineer",
                "ML Engineer", "Data Analyst", "Research Scientist"
            ],
            "DevOps": [
                "DevOps Engineer", "Cloud Engineer", "Infrastructure Engineer",
                "Platform Engineer", "Security Engineer"
            ]
        }
        
        self.technologies = {
            "frontend": [
                {"name": "React", "versions": ["18.x", "17.x"], "purpose": "UI framework"},
                {"name": "Vue.js", "versions": ["3.x", "2.x"], "purpose": "Progressive framework"},
                {"name": "Angular", "versions": ["16.x", "15.x"], "purpose": "Application framework"},
                {"name": "Streamlit", "versions": ["1.28", "1.27"], "purpose": "Python web apps"},
                {"name": "Next.js", "versions": ["13.x", "12.x"], "purpose": "React framework"},
                {"name": "TypeScript", "versions": ["5.x", "4.x"], "purpose": "Type-safe JavaScript"},
                {"name": "Tailwind CSS", "versions": ["3.x"], "purpose": "Utility-first CSS"},
                {"name": "Material-UI", "versions": ["5.x"], "purpose": "React components"},
                {"name": "Bootstrap", "versions": ["5.x"], "purpose": "CSS framework"}
            ],
            "backend": [
                {"name": "Python", "versions": ["3.11", "3.10", "3.9"], "purpose": "Programming language"},
                {"name": "FastAPI", "versions": ["0.104", "0.103"], "purpose": "Modern API framework"},
                {"name": "Django", "versions": ["4.x", "3.x"], "purpose": "Web framework"},
                {"name": "Flask", "versions": ["2.x"], "purpose": "Micro web framework"},
                {"name": "Node.js", "versions": ["20.x", "18.x"], "purpose": "JavaScript runtime"},
                {"name": "Express.js", "versions": ["4.x"], "purpose": "Node.js framework"},
                {"name": "Spring Boot", "versions": ["3.x", "2.x"], "purpose": "Java framework"},
                {"name": "Go", "versions": ["1.21", "1.20"], "purpose": "Programming language"},
                {"name": ".NET Core", "versions": ["7.x", "6.x"], "purpose": "Cross-platform framework"}
            ],
            "database": [
                {"name": "PostgreSQL", "versions": ["15.x", "14.x"], "purpose": "Relational database"},
                {"name": "MongoDB", "versions": ["7.x", "6.x"], "purpose": "Document database"},
                {"name": "Redis", "versions": ["7.x"], "purpose": "In-memory data store"},
                {"name": "MySQL", "versions": ["8.x"], "purpose": "Relational database"},
                {"name": "Elasticsearch", "versions": ["8.x"], "purpose": "Search engine"},
                {"name": "InfluxDB", "versions": ["2.x"], "purpose": "Time series database"}
            ],
            "ai_ml": [
                {"name": "TensorFlow", "versions": ["2.15", "2.14"], "purpose": "ML framework"},
                {"name": "PyTorch", "versions": ["2.1", "2.0"], "purpose": "Deep learning framework"},
                {"name": "Scikit-learn", "versions": ["1.3", "1.2"], "purpose": "ML library"},
                {"name": "OpenAI API", "versions": ["v1"], "purpose": "Language models"},
                {"name": "Azure OpenAI", "versions": ["2023-12-01"], "purpose": "AI services"},
                {"name": "Hugging Face", "versions": ["4.x"], "purpose": "NLP models"},
                {"name": "LangChain", "versions": ["0.1", "0.0"], "purpose": "LLM applications"},
                {"name": "Pandas", "versions": ["2.x"], "purpose": "Data manipulation"},
                {"name": "NumPy", "versions": ["1.24"], "purpose": "Numerical computing"}
            ],
            "cloud": [
                {"name": "AWS", "versions": ["Latest"], "purpose": "Cloud platform"},
                {"name": "Azure", "versions": ["Latest"], "purpose": "Cloud platform"},
                {"name": "Google Cloud", "versions": ["Latest"], "purpose": "Cloud platform"},
                {"name": "Docker", "versions": ["24.x", "23.x"], "purpose": "Containerization"},
                {"name": "Kubernetes", "versions": ["1.28", "1.27"], "purpose": "Container orchestration"},
                {"name": "Terraform", "versions": ["1.6", "1.5"], "purpose": "Infrastructure as code"}
            ],
            "tools": [
                {"name": "Git", "versions": ["2.x"], "purpose": "Version control"},
                {"name": "GitHub", "versions": ["Latest"], "purpose": "Code hosting"},
                {"name": "Jenkins", "versions": ["2.x"], "purpose": "CI/CD"},
                {"name": "GitHub Actions", "versions": ["Latest"], "purpose": "CI/CD"},
                {"name": "Jira", "versions": ["Latest"], "purpose": "Project management"},
                {"name": "Confluence", "versions": ["Latest"], "purpose": "Documentation"},
                {"name": "Slack", "versions": ["Latest"], "purpose": "Communication"},
                {"name": "VS Code", "versions": ["Latest"], "purpose": "Code editor"},
                {"name": "Postman", "versions": ["Latest"], "purpose": "API testing"}
            ]
        }
        
        self.process_types = [
            "Development Workflow", "Code Review Process", "Deployment Process",
            "Testing Process", "Documentation Process", "Security Process",
            "Onboarding Process", "Performance Review", "Meeting Process",
            "Incident Response", "Change Management", "Quality Assurance"
        ]

    def generate_names(self) -> List[str]:
        """Generate realistic employee names."""
        first_names = [
            "Alex", "Jordan", "Sam", "Taylor", "Casey", "Morgan", "Jamie", "Avery",
            "Riley", "Quinn", "Sage", "River", "Phoenix", "Rowan", "Blake", "Cameron",
            "Drew", "Finley", "Hayden", "Kendall", "Logan", "Parker", "Reese", "Skylar",
            "Emerson", "Harper", "Indigo", "Justice", "Kai", "Lane", "Marlowe", "Nova"
        ]
        
        last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
            "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
            "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker"
        ]
        
        return [f"{random.choice(first_names)} {random.choice(last_names)}" for _ in range(50)]

    def generate_member_info(self, num_projects: int = 5, members_per_project: int = 8) -> List[Dict[str, Any]]:
        """Generate comprehensive member information for multiple projects."""
        names = self.generate_names()
        projects = []
        
        for i in range(num_projects):
            project_code = f"PROJ{i+1:03d}"
            project_names = [
                "Employee Onboarding Assistant", "Customer Portal Redesign", 
                "Mobile Banking App", "E-commerce Platform", "Data Analytics Dashboard",
                "Cloud Migration Project", "AI Chatbot System", "Internal Tools Platform",
                "Security Enhancement Project", "Performance Optimization Initiative"
            ]
            
            project = {
                "project_code": project_code,
                "project_name": project_names[i] if i < len(project_names) else f"Project {i+1}",
                "department": random.choice(self.departments),
                "start_date": (datetime.now() - timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"),
                "status": random.choice(["active", "planning", "completed", "on-hold"]),
                "description": f"Strategic initiative to improve business outcomes through technology",
                "members": []
            }
            
            # Generate team members for this project
            project_members = random.sample(names, members_per_project)
            for j, name in enumerate(project_members):
                dept = project["department"]
                available_roles = self.roles.get(dept, ["Team Member", "Specialist", "Coordinator"])
                
                member = {
                    "employee_id": f"EMP{(i*members_per_project + j + 1):04d}",
                    "name": name,
                    "role": random.choice(available_roles),
                    "email": f"{name.lower().replace(' ', '.')}@company.com",
                    "department": dept,
                    "team": f"{dept} Team {random.randint(1, 3)}",
                    "manager": project_members[0] if j > 0 else "Director of " + dept,
                    "hire_date": (datetime.now() - timedelta(days=random.randint(30, 1095))).strftime("%Y-%m-%d"),
                    "location": random.choice(["New York", "San Francisco", "Remote", "London", "Singapore"]),
                    "phone": f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                    "skills": random.sample([
                        "Python", "JavaScript", "React", "Node.js", "AWS", "Docker", 
                        "Kubernetes", "PostgreSQL", "MongoDB", "Machine Learning",
                        "Data Analysis", "Project Management", "Agile", "DevOps"
                    ], random.randint(3, 7)),
                    "status": random.choice(["active", "active", "active", "on-leave"]),
                    "security_clearance": random.choice(["standard", "elevated", "admin"]) if dept == "Engineering" else "standard"
                }
                project["members"].append(member)
            
            projects.append(project)
        
        return projects

    def generate_process_info(self, num_projects: int = 5) -> List[Dict[str, Any]]:
        """Generate detailed process information for projects."""
        projects = []
        
        for i in range(num_projects):
            project_code = f"PROJ{i+1:03d}"
            
            project = {
                "project_code": project_code,
                "project_name": f"Project {i+1}",
                "processes": []
            }
            
            # Generate processes for this project
            process_templates = [
                {
                    "name": "Requirements Gathering",
                    "description": "Collect and document detailed project requirements from stakeholders",
                    "duration_days": 14,
                    "deliverables": ["Requirements Document", "User Stories", "Acceptance Criteria"]
                },
                {
                    "name": "Design & Architecture",
                    "description": "Create system design and technical architecture documentation",
                    "duration_days": 21,
                    "deliverables": ["System Architecture", "Database Design", "API Specifications", "UI/UX Mockups"]
                },
                {
                    "name": "Development Sprint Planning",
                    "description": "Plan development sprints and allocate resources",
                    "duration_days": 3,
                    "deliverables": ["Sprint Backlog", "Resource Allocation", "Timeline"]
                },
                {
                    "name": "Core Development",
                    "description": "Implement core functionality according to specifications",
                    "duration_days": 45,
                    "deliverables": ["Source Code", "Unit Tests", "Integration Tests", "Documentation"]
                },
                {
                    "name": "Quality Assurance",
                    "description": "Comprehensive testing of all system components",
                    "duration_days": 14,
                    "deliverables": ["Test Cases", "Bug Reports", "Performance Reports", "Security Audit"]
                },
                {
                    "name": "User Acceptance Testing",
                    "description": "Stakeholder testing and validation of requirements",
                    "duration_days": 10,
                    "deliverables": ["UAT Results", "User Feedback", "Sign-off Documentation"]
                },
                {
                    "name": "Deployment",
                    "description": "Deploy system to production environment",
                    "duration_days": 5,
                    "deliverables": ["Deployment Plan", "Production Deployment", "Monitoring Setup"]
                },
                {
                    "name": "Post-Launch Support",
                    "description": "Monitor system performance and provide support",
                    "duration_days": 30,
                    "deliverables": ["Performance Reports", "Issue Resolution", "User Support"]
                }
            ]
            
            start_date = datetime.now() - timedelta(days=random.randint(30, 180))
            
            for j, template in enumerate(process_templates):
                process_start = start_date + timedelta(days=sum(p["duration_days"] for p in process_templates[:j]))
                process_end = process_start + timedelta(days=template["duration_days"])
                
                # Determine status based on dates
                now = datetime.now()
                if process_end < now:
                    status = "completed"
                elif process_start < now < process_end:
                    status = "in-progress"
                else:
                    status = "planned"
                
                process = {
                    "process_id": f"PROC{i+1:03d}-{j+1:02d}",
                    "process_name": template["name"],
                    "description": template["description"],
                    "category": random.choice(self.process_types),
                    "status": status,
                    "priority": random.choice(["high", "medium", "low"]),
                    "start_date": process_start.strftime("%Y-%m-%d"),
                    "end_date": process_end.strftime("%Y-%m-%d"),
                    "estimated_hours": template["duration_days"] * random.randint(6, 10),
                    "responsible_members": [f"EMP{random.randint(1, 40):04d}@company.com" for _ in range(random.randint(1, 3))],
                    "stakeholders": [f"EMP{random.randint(1, 40):04d}@company.com" for _ in range(random.randint(1, 2))],
                    "deliverables": template["deliverables"],
                    "dependencies": [f"PROC{i+1:03d}-{max(1, j):02d}"] if j > 0 else [],
                    "next_processes": [f"PROC{i+1:03d}-{j+2:02d}"] if j < len(process_templates)-1 else [],
                    "risks": [
                        "Resource availability constraints",
                        "Technical complexity challenges", 
                        "Timeline dependencies"
                    ][:random.randint(1, 3)],
                    "success_criteria": [
                        "All deliverables completed on time",
                        "Quality standards met",
                        "Stakeholder approval received"
                    ],
                    "progress_percentage": random.randint(0, 100) if status == "in-progress" else (100 if status == "completed" else 0)
                }
                
                project["processes"].append(process)
            
            projects.append(project)
        
        return projects

    def generate_techstack_info(self, num_projects: int = 5) -> List[Dict[str, Any]]:
        """Generate comprehensive technology stack information."""
        projects = []
        
        for i in range(num_projects):
            project_code = f"PROJ{i+1:03d}"
            
            project = {
                "project_code": project_code,
                "project_name": f"Project {i+1}",
                "tech_stack": {},
                "architecture": {
                    "pattern": random.choice(["Microservices", "Monolithic", "Serverless", "Hybrid"]),
                    "deployment": random.choice(["Cloud-native", "On-premise", "Hybrid Cloud"]),
                    "scalability": random.choice(["Horizontal", "Vertical", "Auto-scaling"])
                },
                "development_practices": {
                    "methodology": random.choice(["Agile", "Scrum", "Kanban", "DevOps"]),
                    "version_control": "Git",
                    "ci_cd": random.choice(["GitHub Actions", "Jenkins", "Azure DevOps", "GitLab CI"]),
                    "testing": ["Unit Testing", "Integration Testing", "E2E Testing"],
                    "code_review": "Pull Request based review",
                    "documentation": random.choice(["Confluence", "GitBook", "Notion", "Wiki"])
                },
                "security": {
                    "authentication": random.choice(["OAuth 2.0", "SAML", "JWT", "Multi-factor"]),
                    "authorization": "Role-based Access Control (RBAC)",
                    "data_encryption": "AES-256",
                    "security_scanning": ["SAST", "DAST", "Dependency Scanning"],
                    "compliance": random.choice(["SOC 2", "GDPR", "HIPAA", "PCI DSS"])
                }
            }
            
            # Generate tech stack for each category
            for category, technologies in self.technologies.items():
                selected_techs = random.sample(technologies, random.randint(2, min(6, len(technologies))))
                project["tech_stack"][category] = []
                
                for tech in selected_techs:
                    tech_info = {
                        "technology": tech["name"],
                        "version": random.choice(tech["versions"]),
                        "purpose": tech["purpose"],
                        "status": random.choice(["active", "deprecated", "experimental"]),
                        "documentation_url": f"https://docs.company.com/{tech['name'].lower().replace(' ', '-')}",
                        "support_team": random.choice(["DevOps Team", "Platform Team", "Engineering Team"]),
                        "license": random.choice(["MIT", "Apache 2.0", "Commercial", "Open Source"]),
                        "learning_resources": [
                            f"Internal {tech['name']} Training",
                            f"Official {tech['name']} Documentation",
                            f"Company {tech['name']} Best Practices"
                        ]
                    }
                    project["tech_stack"][category].append(tech_info)
            
            projects.append(project)
        
        return projects

    def generate_chat_history(self, num_conversations: int = 20) -> List[Dict[str, Any]]:
        """Generate realistic chat history examples."""
        conversations = []
        
        sample_conversations = [
            {
                "user": "Who is my team lead?",
                "assistant": "Based on your project assignment, your team lead is Alex Johnson. Alex is a Senior Software Engineer with 5 years of experience and can be reached at alex.johnson@company.com."
            },
            {
                "user": "What's our code review process?",
                "assistant": "Our code review process follows these steps: 1) Create a pull request with detailed description, 2) Assign at least 2 reviewers, 3) Address all feedback, 4) Get approval from senior developer, 5) Merge to main branch. All code must pass automated tests before review."
            },
            {
                "user": "What technologies do we use for frontend development?",
                "assistant": "For frontend development, we primarily use React 18.x with TypeScript for type safety. We also use Tailwind CSS for styling, Next.js for full-stack React applications, and Streamlit for internal Python-based web applications."
            },
            {
                "user": "How do I request time off?",
                "assistant": "To request time off: 1) Submit request through the HR portal at least 2 weeks in advance, 2) Get approval from your direct manager, 3) Update your calendar and set up out-of-office messages, 4) Brief your team on any handover requirements."
            },
            {
                "user": "What's our deployment process?",
                "assistant": "Our deployment process uses CI/CD with GitHub Actions: 1) Code is pushed to feature branch, 2) Automated tests run, 3) Pull request review and approval, 4) Merge triggers staging deployment, 5) Manual approval for production deployment, 6) Monitoring and rollback procedures in place."
            }
        ]
        
        for i in range(num_conversations):
            # Use sample conversations or generate variations
            if i < len(sample_conversations):
                base_conversation = sample_conversations[i]
            else:
                base_conversation = random.choice(sample_conversations)
            
            conversation = {
                "conversation_id": f"CONV{i+1:04d}",
                "user_id": f"EMP{random.randint(1, 40):04d}",
                "timestamp": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
                "messages": [
                    {
                        "role": "user",
                        "content": base_conversation["user"],
                        "timestamp": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
                    },
                    {
                        "role": "assistant", 
                        "content": base_conversation["assistant"],
                        "timestamp": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
                        "tools_used": random.choice([[], ["get_member_information"], ["get_process_information"], ["get_techstack_information"]])
                    }
                ],
                "satisfaction_rating": random.randint(3, 5),
                "resolved": random.choice([True, True, True, False]),
                "topic_tags": random.sample(["onboarding", "team", "process", "technology", "hr", "deployment"], random.randint(1, 3))
            }
            
            conversations.append(conversation)
        
        return conversations

    def save_to_file(self, data: Any, filename: str) -> None:
        """Save data to JSON file with proper formatting."""
        filepath = self.data_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Generated {filename} with {len(data) if isinstance(data, list) else 'structured'} records")

    def generate_all_mock_data(self) -> None:
        """Generate all mock data files."""
        print("🚀 Starting mock data generation...")
        print("=" * 50)
        
        try:
            # Generate member information
            print("👥 Generating member information...")
            member_data = self.generate_member_info(num_projects=5, members_per_project=8)
            self.save_to_file(member_data, "member_info.json")
            
            # Generate process information
            print("📋 Generating process information...")
            process_data = self.generate_process_info(num_projects=5)
            self.save_to_file(process_data, "processes.json")
            
            # Generate tech stack information
            print("🛠️ Generating tech stack information...")
            techstack_data = self.generate_techstack_info(num_projects=5)
            self.save_to_file(techstack_data, "techstack.json")
            
            # Generate chat history
            print("💬 Generating chat history...")
            chat_data = self.generate_chat_history(num_conversations=25)
            self.save_to_file(chat_data, "chat_history.json")
            
            print("=" * 50)
            print("✅ Mock data generation completed successfully!")
            print(f"📁 All files saved to: {self.data_dir.absolute()}")
            
            # Print summary
            print("\n📊 Generated Data Summary:")
            print(f"   • {len(member_data)} projects with member information")
            print(f"   • {sum(len(p['members']) for p in member_data)} total team members")
            print(f"   • {len(process_data)} projects with process information")
            print(f"   • {sum(len(p['processes']) for p in process_data)} total processes")
            print(f"   • {len(techstack_data)} projects with tech stack information")
            print(f"   • {len(chat_data)} conversation examples")
            
        except Exception as e:
            print(f"❌ Error generating mock data: {str(e)}")
            raise

def main():
    """Main function to run the mock data generator."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate mock data for Employee Onboarding Assistant")
    parser.add_argument("--data-dir", default="data", help="Directory to save generated data (default: data)")
    parser.add_argument("--projects", type=int, default=5, help="Number of projects to generate (default: 5)")
    parser.add_argument("--members", type=int, default=8, help="Members per project (default: 8)")
    parser.add_argument("--conversations", type=int, default=25, help="Number of chat conversations (default: 25)")
    
    args = parser.parse_args()
    
    print("🤖 Employee Onboarding Assistant - Mock Data Generator")
    print("=" * 60)
    
    generator = MockDataGenerator(data_dir=args.data_dir)
    
    # Generate with custom parameters if provided
    if args.projects != 5 or args.members != 8 or args.conversations != 25:
        print("📋 Generating member information...")
        member_data = generator.generate_member_info(num_projects=args.projects, members_per_project=args.members)
        generator.save_to_file(member_data, "member_info.json")
        
        print("📋 Generating process information...")
        process_data = generator.generate_process_info(num_projects=args.projects)
        generator.save_to_file(process_data, "processes.json")
        
        print("🛠️ Generating tech stack information...")
        techstack_data = generator.generate_techstack_info(num_projects=args.projects)
        generator.save_to_file(techstack_data, "techstack.json")
        
        print("💬 Generating chat history...")
        chat_data = generator.generate_chat_history(num_conversations=args.conversations)
        generator.save_to_file(chat_data, "chat_history.json")
        
        print("✅ Mock data generation completed!")
    else:
        # Use default generation
        generator.generate_all_mock_data()

if __name__ == "__main__":
    main()
