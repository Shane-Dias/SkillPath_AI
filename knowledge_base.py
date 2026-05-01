"""
Custom Expert System for Skill Gap Analysis
Implements CO3 (Knowledge Representation) & CO4 (Expert System)
No external dependencies - works with Python 3.10+
"""

from typing import Dict, List, Set, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum

class Importance(Enum):
    CRITICAL = "critical"
    IMPORTANT = "important"
    NICE_TO_HAVE = "nice-to-have"

class Proficiency(Enum):
    NONE = "none"
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    
    def get_value(self):
        values = {"none": 0, "beginner": 1, "intermediate": 2, "advanced": 3}
        return values[self.value]

@dataclass
class Fact:
    """Base class for all facts in the expert system"""
    fact_type: str
    data: Dict[str, Any]

@dataclass
class SkillFact(Fact):
    """Skill fact representation"""
    name: str
    level: Proficiency
    
    def __init__(self, name: str, level: str):
        super().__init__("skill", {})
        self.name = name
        self.level = Proficiency(level.lower())

@dataclass
class JobGoalFact(Fact):
    """Job goal fact"""
    title: str
    
    def __init__(self, title: str):
        super().__init__("job_goal", {})
        self.title = title

@dataclass
class MissingSkillFact(Fact):
    """Missing skill fact (inferred)"""
    name: str
    importance: Importance
    current_level: Proficiency
    required_level: Proficiency
    
    def __init__(self, name: str, importance: str, current_level: str, required_level: str):
        super().__init__("missing_skill", {})
        self.name = name
        self.importance = Importance(importance)
        self.current_level = Proficiency(current_level)
        self.required_level = Proficiency(required_level)

@dataclass
class LearningResourceFact(Fact):
    """Learning resource fact"""
    skill: str
    resource_type: str
    url: str
    estimated_hours: int
    
    def __init__(self, skill: str, resource_type: str, url: str, hours: int):
        super().__init__("learning_resource", {})
        self.skill = skill
        self.resource_type = resource_type
        self.url = url
        self.estimated_hours = hours

@dataclass
class CareerPathFact(Fact):
    """Career path fact"""
    current_job: str
    next_job: str
    required_skills: List[str]
    
    def __init__(self, current_job: str, next_job: str, required_skills: List[str]):
        super().__init__("career_path", {})
        self.current_job = current_job
        self.next_job = next_job
        self.required_skills = required_skills

class KnowledgeEngine:
    """
    Custom Expert System Engine
    Implements forward chaining rule-based inference
    """
    
    def __init__(self):
        self.facts: List[Fact] = []
        self.job_requirements = self._load_job_requirements()
        self.learning_resources = self._load_learning_resources()
        self.career_paths = self._load_career_paths()
        
    def _load_job_requirements(self) -> Dict:
        """Knowledge Base: Job requirements"""
        return {
            "Data Scientist": {
                "required_skills": {
                    "Python": "advanced",
                    "SQL": "intermediate",
                    "Machine Learning": "advanced",
                    "Statistics": "intermediate",
                    "Data Visualization": "intermediate",
                    "Big Data": "intermediate"
                },
                "soft_skills": ["Problem Solving", "Communication", "Business Acumen"],
                "education": ["MS/PhD in CS/Statistics", "Data Science Bootcamp"],
                "experience_years": 2
            },
            "Machine Learning Engineer": {
                "required_skills": {
                    "Python": "advanced",
                    "TensorFlow/PyTorch": "advanced",
                    "SQL": "intermediate",
                    "Docker": "intermediate",
                    "Git": "intermediate",
                    "Cloud Platforms": "intermediate",
                    "MLOps": "beginner"
                },
                "soft_skills": ["System Design", "Code Review", "Team Collaboration"],
                "education": ["CS Degree", "ML Certification"],
                "experience_years": 2
            },
            "AI Research Scientist": {
                "required_skills": {
                    "Python": "advanced",
                    "Deep Learning": "advanced",
                    "Mathematics": "advanced",
                    "Research Methods": "advanced",
                    "Paper Writing": "intermediate",
                    "C++": "intermediate"
                },
                "soft_skills": ["Critical Thinking", "Innovation", "Academic Writing"],
                "education": ["PhD in AI/ML", "Research Publications"],
                "experience_years": 3
            },
            "Software Engineer": {
                "required_skills": {
                    "Python/Java": "advanced",
                    "Data Structures": "advanced",
                    "Algorithms": "advanced",
                    "Git": "intermediate",
                    "Databases": "intermediate",
                    "System Design": "intermediate"
                },
                "soft_skills": ["Teamwork", "Agile Methodology", "Code Documentation"],
                "education": ["CS Degree", "Coding Bootcamp"],
                "experience_years": 1
            },
            "Data Analyst": {
                "required_skills": {
                    "SQL": "advanced",
                    "Excel": "advanced",
                    "Python": "intermediate",
                    "Tableau/PowerBI": "intermediate",
                    "Statistics": "intermediate"
                },
                "soft_skills": ["Storytelling", "Business Communication"],
                "education": ["Bachelor's in Analytics/CS"],
                "experience_years": 1
            },
            "DevOps Engineer": {
                "required_skills": {
                    "Linux": "advanced",
                    "Docker": "advanced",
                    "Kubernetes": "intermediate",
                    "CI/CD": "intermediate",
                    "AWS/Azure": "intermediate",
                    "Python/Bash": "intermediate"
                },
                "soft_skills": ["Automation", "Monitoring", "Security"],
                "education": ["CS Degree", "DevOps Certification"],
                "experience_years": 2
            },
            "Frontend Developer": {
                "required_skills": {
                    "JavaScript": "advanced",
                    "React/Vue": "advanced",
                    "HTML/CSS": "advanced",
                    "Git": "intermediate",
                    "Web Performance": "intermediate"
                },
                "soft_skills": ["UI/UX Understanding", "Cross-browser Testing"],
                "education": ["CS Degree", "Bootcamp"],
                "experience_years": 1
            },
            "Backend Developer": {
                "required_skills": {
                    "Python/Java/Node.js": "advanced",
                    "Databases": "advanced",
                    "API Design": "advanced",
                    "System Design": "intermediate",
                    "Docker": "intermediate"
                },
                "soft_skills": ["Security Awareness", "Documentation"],
                "education": ["CS Degree"],
                "experience_years": 2
            }
        }
    
    def _load_learning_resources(self) -> Dict:
        """Knowledge Base: Learning resources"""
        return {
            "Python": [
                {"type": "Course", "name": "Python for Everybody (Coursera)", "hours": 40, "url": "coursera.org/python"},
                {"type": "Book", "name": "Automate the Boring Stuff", "hours": 20, "url": "automatetheboringstuff.com"},
                {"type": "Practice", "name": "LeetCode Python Problems", "hours": 30, "url": "leetcode.com"}
            ],
            "Machine Learning": [
                {"type": "Course", "name": "Andrew Ng ML Course", "hours": 60, "url": "coursera.org/ml"},
                {"type": "Book", "name": "Hands-On ML with Scikit-Learn", "hours": 50, "url": "oreilly.com"}
            ],
            "SQL": [
                {"type": "Course", "name": "SQL for Data Science", "hours": 30, "url": "coursera.org/sql"},
                {"type": "Practice", "name": "LeetCode SQL Problems", "hours": 20, "url": "leetcode.com"}
            ],
            "Deep Learning": [
                {"type": "Course", "name": "Deep Learning Specialization", "hours": 80, "url": "coursera.org/deeplearning"},
                {"type": "Book", "name": "Deep Learning with Python", "hours": 40, "url": "manning.com"}
            ],
            "Docker": [
                {"type": "Course", "name": "Docker Mastery", "hours": 25, "url": "udemy.com/docker"}
            ],
            "Statistics": [
                {"type": "Course", "name": "Statistics with Python", "hours": 40, "url": "coursera.org/statistics"}
            ],
            "Data Visualization": [
                {"type": "Course", "name": "Data Visualization with Python", "hours": 25, "url": "coursera.org/dataviz"}
            ],
            "TensorFlow/PyTorch": [
                {"type": "Course", "name": "Deep Learning Frameworks", "hours": 50, "url": "coursera.org/tensorflow"}
            ],
            "Git": [
                {"type": "Course", "name": "Git & GitHub", "hours": 15, "url": "github.com/git-cheat-sheet"}
            ],
            "Cloud Platforms": [
                {"type": "Course", "name": "AWS Cloud Practitioner", "hours": 30, "url": "aws.amazon.com/training"}
            ],
            "JavaScript": [
                {"type": "Course", "name": "JavaScript: The Good Parts", "hours": 25, "url": "udemy.com/javascript"}
            ],
            "React/Vue": [
                {"type": "Course", "name": "Modern React with Hooks", "hours": 40, "url": "reactjs.org/docs"}
            ]
        }
    
    def _load_career_paths(self) -> Dict:
        """Knowledge Base: Career progression"""
        return {
            "Software Engineer": ["Senior Software Engineer", "Tech Lead", "Engineering Manager"],
            "Data Analyst": ["Senior Data Analyst", "Data Scientist", "Analytics Manager"],
            "Data Scientist": ["Senior Data Scientist", "Lead Data Scientist", "AI Research Scientist"],
            "Machine Learning Engineer": ["Senior MLE", "ML Architect", "AI Director"],
            "DevOps Engineer": ["Senior DevOps", "Cloud Architect", "Platform Engineer"],
            "Frontend Developer": ["Senior Frontend", "Frontend Architect", "Full Stack Developer"],
            "Backend Developer": ["Senior Backend", "Backend Architect", "System Architect"]
        }
    
    def declare(self, fact: Fact):
        """Add a fact to the working memory"""
        self.facts.append(fact)
    
    def reset(self):
        """Clear all facts"""
        self.facts = []
    
    def get_facts_by_type(self, fact_type: str) -> List[Fact]:
        """Get all facts of a specific type"""
        return [f for f in self.facts if f.fact_type == fact_type]
    
    def run(self):
        """
        Run the inference engine
        Implements forward chaining rule application
        """
        # Rule 1: Analyze skill gaps for existing skills
        self._apply_skill_gap_rule()
        
        # Rule 2: Identify completely missing skills
        self._apply_missing_skills_rule()
        
        # Rule 3: Suggest learning resources for missing skills
        self._apply_learning_resources_rule()
        
        # Rule 4: Suggest career progression
        self._apply_career_progression_rule()
    
    def _apply_skill_gap_rule(self):
        """Rule: IF skill level < required level THEN declare missing skill"""
        job_goals = self.get_facts_by_type("job_goal")
        skills = self.get_facts_by_type("skill")
        
        for job_goal in job_goals:
            job_title = job_goal.title
            if job_title in self.job_requirements:
                required_skills = self.job_requirements[job_title]["required_skills"]
                
                for skill in skills:
                    # Check if this skill is required for the job
                    for req_skill, req_level in required_skills.items():
                        if skill.name.lower() == req_skill.lower() or req_skill.lower() in skill.name.lower():
                            current_level_value = skill.level.get_value()
                            required_level_value = Proficiency(req_level).get_value()
                            
                            if current_level_value < required_level_value:
                                importance = "critical" if req_level == "advanced" else "important"
                                missing_fact = MissingSkillFact(
                                    name=req_skill,
                                    importance=importance,
                                    current_level=skill.level.value,
                                    required_level=req_level
                                )
                                # Check if already declared
                                if not self._fact_exists(missing_fact):
                                    self.facts.append(missing_fact)
    
    def _apply_missing_skills_rule(self):
        """Rule: IF required skill not in existing skills THEN declare missing"""
        job_goals = self.get_facts_by_type("job_goal")
        existing_skills = {s.name.lower() for s in self.get_facts_by_type("skill")}
        
        for job_goal in job_goals:
            job_title = job_goal.title
            if job_title in self.job_requirements:
                required_skills = self.job_requirements[job_title]["required_skills"]
                
                for skill, req_level in required_skills.items():
                    if skill.lower() not in existing_skills:
                        importance = "critical" if req_level == "advanced" else "important"
                        missing_fact = MissingSkillFact(
                            name=skill,
                            importance=importance,
                            current_level="none",
                            required_level=req_level
                        )
                        if not self._fact_exists(missing_fact):
                            self.facts.append(missing_fact)
    
    def _apply_learning_resources_rule(self):
        """Rule: IF missing skill THEN suggest learning resources"""
        missing_skills = self.get_facts_by_type("missing_skill")
        
        for missing in missing_skills:
            if missing.name in self.learning_resources:
                resources = self.learning_resources[missing.name]
                for resource in resources[:2]:  # Top 2 resources
                    resource_fact = LearningResourceFact(
                        skill=missing.name,
                        resource_type=resource["type"],
                        url=resource["url"],
                        hours=resource["hours"]
                    )
                    if not self._fact_exists(resource_fact):
                        self.facts.append(resource_fact)
    
    def _apply_career_progression_rule(self):
        """Rule: IF current job known THEN suggest next career steps"""
        skills = self.get_facts_by_type("skill")
        
        # Infer current job based on skills (simplified)
        for skill in skills:
            # This is a simplified inference - in reality would be more complex
            pass
        
        # For demo purposes, suggest paths based on common patterns
        for current_job, next_jobs in self.career_paths.items():
            for next_job in next_jobs[:2]:
                if next_job in self.job_requirements:
                    path_fact = CareerPathFact(
                        current_job=current_job,
                        next_job=next_job,
                        required_skills=list(self.job_requirements[next_job].get("required_skills", {}).keys())
                    )
                    if not self._fact_exists(path_fact):
                        self.facts.append(path_fact)
    
    def _fact_exists(self, new_fact: Fact) -> bool:
        """Check if a fact already exists in working memory"""
        for fact in self.facts:
            if fact.fact_type == new_fact.fact_type:
                # Compare attributes
                if hasattr(fact, '__dict__') and hasattr(new_fact, '__dict__'):
                    if fact.__dict__ == new_fact.__dict__:
                        return True
        return False