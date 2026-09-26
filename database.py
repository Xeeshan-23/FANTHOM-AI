"""
Mock database seeded with realistic meeting recordings, timestamped transcripts,
and pre-generated summaries to satisfy the 8x assignment data requirements.
"""

MEETINGS_DB = {
    "meet-001": {
        "id": "meet-001",
        "title": "Google Product Manager Prioritization Interview",
        "date": "2026-09-24T14:30:00Z",
        "duration": "17m 08s",
        "participants": ["Tilt Brush (PMM)", "Cherrie (Interviewee)"],
        "video_url": "https://www.youtube.com/embed/vApI2SSxxUA?start=23&enablejsapi=1&origin=http://127.0.0.1:8000",
        "raw_transcript": (
            "[00:00 - 01:14] Introduction and Clarification: The interviewee, Cherrie, confirms her role as the PM for Tilt Brush and outlines her plan to walk through prioritization themes, criteria, and a practical application of these frameworks.\n"
            "[01:14 - 06:42] Strategic Themes: Cherrie discusses the current state of the VR market, estimating a relatively small active user base. She shifts the product's focus from monetization toward user acquisition, engagement, and exploration of the VR medium.\n"
            "[06:42 - 12:29] Prioritization Framework: She introduces three main criteria buckets for feature prioritization: Impact (Focused on user value and long-term product health), Urgency (Evaluating external timelines, marketing, and dependencies), and Effort (Assessing the engineering resources and time required to build).\n"
            "[12:29 - 16:10] Collaboration: Cherrie emphasizes that while the PM is the decision-maker, effective prioritization is a collaborative process involving the team, rather than a top-down mandate."
        ),
        "summary": {
            "executive_summary": "Cherrie outlined her product management approach for Tilt Brush, focusing on user acquisition and engagement over immediate monetization due to the small VR market size. She detailed a prioritization framework based on Impact, Urgency, and Effort, emphasizing that prioritization must be a collaborative team process.",
            "key_decisions": [
                "Shift product focus toward user acquisition and exploration rather than short-term monetization.",
                "Adopt a three-pillar prioritization framework evaluating Impact, Urgency, and Effort."
            ],
            "action_items": [
                {"task": "Evaluate upcoming VR features against the new Impact/Urgency/Effort criteria", "assignee": "Cherrie", "completed": False},
                {"task": "Align engineering and design teams on the collaborative prioritization workflow", "assignee": "Cherrie", "completed": False}
            ]
        }
    },
    "meet-002": {
        "id": "meet-002",
        "title": "Technical Interview: Core Python & OOP",
        "date": "2026-09-25T11:00:00Z",
        "duration": "10m 05s",
        "participants": ["Interviewer", "Zeeshan (Candidate)"],
        "video_url": "https://www.youtube.com/embed/0HYv2GvfyC8?enablejsapi=1&origin=http://127.0.0.1:8000",
        "raw_transcript": (
            "[01:55] Interviewer: Let's move on to some practical Python skills. Can you write a function to check if a string is a palindrome?\n"
            "[01:59] Zeeshan: Sure, the simplest way is to reverse the string using slicing and compare it to the original.\n"
            "[02:56] Interviewer: Good. Now, how would you efficiently remove duplicate elements from a list?\n"
            "[03:00] Zeeshan: I would convert the list into a set, which automatically removes duplicates, and then cast it back to a list.\n"
            "[04:21] Interviewer: Let's talk about data structures. What can you tell me about Python dictionaries? Are they mutable or immutable?\n"
            "[04:34] Zeeshan: Dictionaries are immutable.\n"
            "[05:46] Interviewer: Actually, while dictionary keys must be of an immutable type, the dictionaries themselves and their values are mutable. You can change them after creation.\n"
            "[06:05] Interviewer: Let's shift to memory management. Can you explain garbage collection?\n"
            "[06:33] Zeeshan: Yes, in languages like Java, the garbage collector automatically frees up memory by destroying objects that are no longer being referenced by the application.\n"
            "[06:57] Interviewer: Finally, let's cover Object-Oriented Programming. What are the four pillars of OOP?\n"
            "[07:15] Zeeshan: They are abstraction, polymorphism, encapsulation, and inheritance.\n"
            "[08:37] Interviewer: Can you explain method overriding and its relationship to polymorphism?\n"
            "[09:53] Zeeshan: Method overriding is a form of runtime polymorphism where a child class provides a specific implementation of a method that is already defined in its parent class."
        ),
        "summary": {
            "executive_summary": "Conducted a technical interview covering core Python skills, memory management, and Object-Oriented Programming. The candidate successfully solved practical coding challenges and clearly defined OOP principles, though required a minor correction regarding the mutability of Python dictionaries.",
            "key_decisions": [
                "Proceed with evaluation based on strong understanding of OOP fundamentals and practical list/string operations."
            ],
            "action_items": [
                {"task": "Submit technical scorecard for the Python engineering interview", "assignee": "Interviewer", "completed": False},
                {"task": "Brush up on Python-specific data structure mutability rules", "assignee": "Zeeshan", "completed": False}
            ]
        }
    },
    "meet-003": {
        "id": "meet-003",
        "title": "LLM Architecture & Deployment Strategy",
        "date": "2026-09-24T15:00:00Z",
        "duration": "08m 15s",
        "participants": ["Sarah (Lead)", "Zeeshan (AI Engineer)"],
        "video_url": "https://www.youtube.com/embed/MbnuZRgAN8E?start=25&enablejsapi=1&origin=http://127.0.0.1:8000",
        "raw_transcript": (
            "[02:35] Sarah: Before we lock in the new model, we need to ensure the data pipeline handles tokenization correctly to avoid the accuracy drops we saw last week.\n"
            "[03:15] Zeeshan: Absolutely. The key is strict enforcement—we have to use the exact tokenizer associated with the specific HuggingFace model, otherwise the embeddings get misaligned and the model outputs garbage.\n"
            "[04:30] Sarah: Understood. Regarding the model architecture itself, are we still debating between BERT and a GPT-style model for this feature?\n"
            "[05:10] Zeeshan: It depends on the primary task. BERT is a bidirectional encoder, which makes it perfect for understanding context, classification, or search. But since this feature requires text generation, we need to go with a decoder-only architecture like GPT.\n"
            "[06:31] Sarah: Makes sense. Let's talk deployment. How quickly can we get a prototype in front of the stakeholders?\n"
            "[07:15] Zeeshan: I can spin up a UI using Streamlit by tomorrow for the initial demo. Once it's approved, we will containerize it and move the production deployment over to AWS."
        ),
        "summary": {
            "executive_summary": "The team discussed LLM implementation details, emphasizing the critical need to match tokenizers precisely with their associated models. They agreed on using a decoder-only GPT architecture for the upcoming text generation feature and outlined a two-phase deployment strategy.",
            "key_decisions": [
                "Select a decoder-only (GPT-style) model architecture over BERT to support text generation requirements.",
                "Utilize Streamlit for rapid internal prototyping before migrating to AWS for the final production deployment."
            ],
            "action_items": [
                {"task": "Verify tokenizer alignment in the data preprocessing pipeline", "assignee": "Zeeshan", "completed": False},
                {"task": "Build and deploy the initial Streamlit demo for stakeholder review", "assignee": "Zeeshan", "completed": False}
            ]
        }
    }
}


def get_all_meetings():
    """Retrieve summary metadata for all meetings."""
    return [
        {
            "id": m["id"],
            "title": m["title"],
            "date": m["date"],
            "duration": m["duration"],
            "participants": m["participants"],
            "snippet": m["summary"]["executive_summary"]
        }
        for m in MEETINGS_DB.values()
    ]


def get_meeting_by_id(meeting_id: str):
    """Retrieve full details for a specific meeting."""
    return MEETINGS_DB.get(meeting_id)


def save_meeting_summary(meeting_id: str, summary_data: dict):
    """Update meeting summary with newly generated AI output."""
    if meeting_id in MEETINGS_DB:
        MEETINGS_DB[meeting_id]["summary"] = summary_data
        return True
    return False