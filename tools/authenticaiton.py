from typing import Any, Dict, Optional
import os

def user_data(Name: str, TC_Kimlik: str) -> Optional[Dict[str, Any]]:
    """
    mock user data retrieval.

    Args:
        Name (str): The name of the user.
        TC_Kimlik (str): The Turkish ID number of the user.
    
    Returns:
        Optional[Dict[str, Any]]: A dictionary containing user details if authentication is successful, None otherwise.
    """
    Name = Name.strip().upper()
    TC_Kimlik = TC_Kimlik.strip()

    # Simulated database of users
    users_db = {
        "12345678901": {"Name": "ALİ VELİ"},
        "10987654321": {"Name": "AYŞE DEMİR"},
        "11223344556": {"Name": "MEHMET YILMAZ"},
        "22334455667": {"Name": "FATMA YILMAZ"},
        "66554433221": {"Name": "ELİF ÇELİK"},
        "99887766554": {"Name": "HÜSEYİN KAYA"},
        "55667788990": {"Name": "ZÜMRÜT ŞEN"},
        "33445566778": {"Name": "CANAN GÜL"},
        "77889900112": {"Name": "SERKAN ÖZTÜRK"},
        "44556677889": {"Name": "NİHAL AKIN"},
        "12312312312": {"Name": "MUSTAFA KARA"},
        "32132132132": {"Name": "SEVİM YILDIRIM"},
        "45645645645": {"Name": "TUNCAY ÇAKIR"},
        "65465465465": {"Name": "DİLEK ARSLAN"},
        "78978978978": {"Name": "RAMAZAN POLAT"},
        "98798798798": {"Name": "GÜLŞAH KORKMAZ"},
        "14725836914": {"Name": "YUSUF DEMİR"},
        "36925814736": {"Name": "SELİN ŞAHİN"},
    }

    user = users_db.get(TC_Kimlik)
    if user and user["Name"] == Name:
        return {"Name": Name, "TC_Kimlik": TC_Kimlik}   
    
    return None

def authenticate_user(Name: str, TC_Kimlik: str) -> bool:
    """
    Authenticate user based on name and Turkish ID number.

    Args:
        Name (str): The name of the user.
        TC_Kimlik (str): The Turkish ID number of the user.
    
    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    user = user_data(Name, TC_Kimlik)
    return user is not None
    