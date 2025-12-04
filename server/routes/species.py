from fastapi import APIRouter, HTTPException
from playwright.sync_api import sync_playwright
from services.bird_metadata import get_species_image_url


router = APIRouter(
    prefix="/species",
    tags=["Species"]
)


@router.get("/image/{bird_code}")
def get_bird_image(bird_code: str):
    """
    fetch image URL for a specific bird code.
    added in case we want to fetch images on-demand for specific birds.
    
    args:
        bird_code: eBird bird code (ex. 'amecro' for American Crow)
    
    returns:
        json with bird_code and imageUrl
    """
    
    try:
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            image_url = get_species_image_url(bird_code, browser_page=page)
            return {"birdCode": bird_code, "imageUrl": image_url}
        finally:
            browser.close()
            playwright.stop()
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"failed to fetch image: {str(e)}")
