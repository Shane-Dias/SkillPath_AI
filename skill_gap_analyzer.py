"""
Skill Gap Analyzer - Handles analysis logic
"""

from knowledge_base import (
    KnowledgeEngine, SkillFact, JobGoalFact, 
    MissingSkillFact, LearningResourceFact, CareerPathFact,
    Proficiency, Importance
)
from typing import Dict, List
from tabulate import tabulate

class SkillGapAnalyzer:
    """Main analyzer class for skill gap analysis"""
    
    def __init__(self):
        self.expert_system = KnowledgeEngine()
        
    def analyze_skills(self, current_skills: Dict[str, str], dream_job: str) -> Dict:
        """
        Analyze skill gap and return comprehensive analysis
        """
        # Reset the expert system
        self.expert_system.reset()
        
        # Declare facts
        for skill, level in current_skills.items():
            self.expert_system.declare(SkillFact(skill, level))
        
        self.expert_system.declare(JobGoalFact(dream_job))
        
        # Run the inference engine
        self.expert_system.run()
        
        # Extract results
        missing_skills = []
        learning_resources = []
        career_paths = []
        
        for fact in self.expert_system.facts:
            if isinstance(fact, MissingSkillFact):
                missing_skills.append({
                    "name": fact.name,
                    "importance": fact.importance.value,
                    "current_level": fact.current_level.value,
                    "required_level": fact.required_level.value
                })
            elif isinstance(fact, LearningResourceFact):
                learning_resources.append({
                    "skill": fact.skill,
                    "type": fact.resource_type,
                    "url": fact.url,
                    "hours": fact.estimated_hours
                })
            elif isinstance(fact, CareerPathFact):
                career_paths.append({
                    "current": fact.current_job,
                    "next": fact.next_job,
                    "skills_needed": fact.required_skills[:3]
                })
        
        # Remove duplicates
        missing_skills = self._deduplicate(missing_skills, "name")
        learning_resources = self._deduplicate(learning_resources, "skill", "type")
        
        # Generate learning path
        learning_path = self._generate_learning_path(missing_skills, learning_resources)
        
        # Calculate readiness score
        job_data = self.expert_system.job_requirements.get(dream_job, {})
        total_required = len(job_data.get("required_skills", {}))
        missing_count = len(missing_skills)
        readiness_score = max(0, (total_required - missing_count) / total_required * 100) if total_required > 0 else 0
        
        return {
            "dream_job": dream_job,
            "missing_skills": missing_skills,
            "learning_resources": learning_resources,
            "learning_path": learning_path,
            "readiness_score": round(readiness_score, 1),
            "total_skills_required": total_required,
            "career_paths": career_paths,
            "job_requirements": job_data
        }
    
    def _deduplicate(self, items, *keys):
        """Remove duplicate items based on keys"""
        seen = set()
        unique_items = []
        for item in items:
            identifier = tuple(item.get(key) for key in keys)
            if identifier not in seen:
                seen.add(identifier)
                unique_items.append(item)
        return unique_items
    
    def _generate_learning_path(self, missing_skills, learning_resources) -> List[Dict]:
        """Generate a structured learning path"""
        critical = [s for s in missing_skills if s['importance'] == 'critical']
        important = [s for s in missing_skills if s['importance'] == 'important']
        
        learning_path = []
        
        if critical:
            learning_path.append({
                "phase": 1,
                "title": "Critical Skills (Prerequisites)",
                "skills": [s['name'] for s in critical],
                "estimated_weeks": len(critical) * 2,
                "resources": [r for r in learning_resources if r['skill'] in [s['name'] for s in critical]]
            })
        
        if important:
            learning_path.append({
                "phase": 2,
                "title": "Important Skills (Core Competencies)",
                "skills": [s['name'] for s in important],
                "estimated_weeks": len(important) * 1,
                "resources": [r for r in learning_resources if r['skill'] in [s['name'] for s in important]]
            })
        
        return learning_path
    
    def display_analysis(self, analysis: Dict):
        """Display analysis results in a formatted way"""
        
        print("\n" + "="*70)
        print(f"🎯 SKILL GAP ANALYSIS FOR: {analysis['dream_job'].upper()}")
        print("="*70)
        
        if 'job_requirements' in analysis and analysis['job_requirements']:
            print(f"\n📋 JOB REQUIREMENTS OVERVIEW:")
            req_skills = analysis['job_requirements'].get('required_skills', {})
            print(f"   Required Skills: {', '.join(req_skills.keys())}")
            print(f"   Experience Needed: {analysis['job_requirements'].get('experience_years', 'N/A')} years")
            print(f"   Education: {', '.join(analysis['job_requirements'].get('education', ['N/A']))}")
        
        print(f"\n📊 READINESS SCORE: {analysis['readiness_score']}%")
        score_bar = "█" * int(analysis['readiness_score'] / 10) + "░" * (10 - int(analysis['readiness_score'] / 10))
        print(f"   [{score_bar}]")
        skills_acquired = analysis['total_skills_required'] - len(analysis['missing_skills'])
        print(f"   Skills Acquired: {skills_acquired}/{analysis['total_skills_required']}")
        
        if analysis['missing_skills']:
            print("\n🔴 MISSING SKILLS:")
            table_data = []
            for skill in analysis['missing_skills']:
                importance_icon = "🔥" if skill['importance'] == 'critical' else "📌"
                current_display = skill['current_level'] if skill['current_level'] != 'none' else '❌ Not acquired'
                table_data.append([
                    skill['name'],
                    f"{importance_icon} {skill['importance'].upper()}",
                    current_display,
                    f"→ {skill['required_level'].upper()}"
                ])
            print(tabulate(table_data, headers=["Skill", "Importance", "Current Level", "Required Level"], tablefmt="grid"))
        else:
            print("\n✅ CONGRATULATIONS! No missing skills found!")
        
        if analysis['learning_path']:
            print("\n📚 RECOMMENDED LEARNING PATH:")
            for phase in analysis['learning_path']:
                print(f"\n  ═══ Phase {phase['phase']}: {phase['title']} ═══")
                print(f"  ⏱️  Estimated time: {phase['estimated_weeks']} weeks")
                for skill in phase['skills']:
                    print(f"\n    🎯 {skill}")
                    resources = [r for r in phase['resources'] if r['skill'] == skill]
                    for res in resources:
                        print(f"       📖 {res['type']}: {res['url']}")
                        print(f"          ⏰ {res['hours']} hours recommended")
        
        if analysis['career_paths']:
            print("\n🚀 SUGGESTED CAREER PROGRESSION:")
            for path in analysis['career_paths']:
                print(f"   {path['current']} → {path['next']}")
        
        print("\n" + "-"*70)
        total_hours = sum(r['hours'] for r in analysis['learning_resources'])
        if total_hours > 0:
            weeks_study = total_hours / 10
            months_study = weeks_study / 4
            print(f"📈 LEARNING SUMMARY:")
            print(f"   📚 Total learning hours: ~{total_hours} hours")
            print(f"   📅 Recommended timeline: {weeks_study:.0f} weeks ({months_study:.1f} months)")
        
        print("="*70 + "\n")