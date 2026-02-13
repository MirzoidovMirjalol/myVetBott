"""
Symptom checking service
"""

from typing import Dict, List


def analyze_symptoms(symptoms_text: str, pet_type: str = "unknown") -> str:
    """
    Analyze pet symptoms and provide basic recommendations
    
    Args:
        symptoms_text: Description of symptoms
        pet_type: Type of pet (dog, cat, etc.)
    
    Returns:
        Recommendations text
    
    Note:
        This is a basic rule-based system. For production, consider
        integrating with a veterinary API or ML model.
    """
    symptoms_lower = symptoms_text.lower()
    response = "🩺 <b>Рекомендации по симптомам:</b>\n\n"
    
    # Check for digestive issues
    if any(word in symptoms_lower for word in ['рвота', 'понос', 'диарея', 'vomit', 'diarrhea']):
        response += "⚠️ <b>Симптомы могут указывать на отравление или инфекцию.</b>\n"
        response += "• Обеспечьте доступ к воде\n"
        response += "• Не кормите 12-24 часа\n"
        response += "• Срочно обратитесь к ветеринару\n\n"
    
    # Check for appetite issues
    elif any(word in symptoms_lower for word in ['не ест', 'аппетит', 'отказ', 'not eating', 'appetite']):
        response += "⚠️ <b>Отказ от еды может быть признаком различных заболеваний.</b>\n"
        response += "• Проверьте температуру\n"
        response += "• Предложите любимое лакомство\n"
        response += "• Если не ест более 24 часов - к врачу\n\n"
    
    # Check for skin issues
    elif any(word in symptoms_lower for word in ['чешется', 'зуд', 'аллергия', 'itching', 'scratch', 'allergy']):
        response += "⚠️ <b>Возможна аллергия или кожное заболевание.</b>\n"
        response += "• Проверьте на блох и клещей\n"
        response += "• Исключите новые продукты\n"
        response += "• Консультация дерматолога\n\n"
    
    # Check for respiratory issues
    elif any(word in symptoms_lower for word in ['кашель', 'чихает', 'дышит', 'cough', 'sneeze', 'breathing']):
        response += "⚠️ <b>Проблемы с дыханием требуют внимания.</b>\n"
        response += "• Проверьте температуру\n"
        response += "• Обеспечьте покой\n"
        response += "• При затрудненном дыхании - срочно к врачу\n\n"
    
    # Check for pain/discomfort
    elif any(word in symptoms_lower for word in ['боль', 'хромает', 'скулит', 'pain', 'limping', 'whining']):
        response += "⚠️ <b>Признаки боли или дискомфорта.</b>\n"
        response += "• Ограничьте физическую активность\n"
        response += "• Осмотрите на наличие травм\n"
        response += "• Консультация ветеринара обязательна\n\n"
    
    # General recommendations
    else:
        response += "ℹ️ <b>Общие рекомендации:</b>\n"
        response += "• Наблюдайте за состоянием\n"
        response += "• Измерьте температуру\n"
        response += "• При ухудшении - обратитесь к ветеринару\n\n"
    
    response += "<b>⚠️ ВНИМАНИЕ:</b> Это только общие рекомендации. "
    response += "Для точного диагноза обратитесь к ветеринару!"
    
    return response


def get_emergency_symptoms() -> List[str]:
    """
    Get list of emergency symptoms that require immediate attention
    
    Returns:
        List of emergency symptom keywords
    """
    return [
        'кровь', 'blood', 'судороги', 'seizure', 'не дышит', 'not breathing',
        'потеря сознания', 'unconscious', 'травма', 'injury', 'яд', 'poison'
    ]


def is_emergency(symptoms_text: str) -> bool:
    """
    Check if symptoms indicate an emergency
    
    Args:
        symptoms_text: Description of symptoms
    
    Returns:
        True if emergency symptoms detected
    """
    symptoms_lower = symptoms_text.lower()
    emergency_keywords = get_emergency_symptoms()
    
    return any(keyword in symptoms_lower for keyword in emergency_keywords)
