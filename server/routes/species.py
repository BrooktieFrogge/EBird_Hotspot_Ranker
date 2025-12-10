from fastapi import APIRouter, HTTPException
from playwright.async_api import async_playwright
from services.bird_metadata import get_species_image_url


router = APIRouter(
    prefix="/species",
    tags=["Species"]
)


@router.get("/image/{bird_code}")
async def get_bird_image(bird_code: str):
    """
    fetch image URL for a specific bird code.
    added in case we want to fetch images on-demand for specific birds.
    
    args:
        bird_code: eBird bird code (ex. 'amecro' for American Crow)
    
    returns:
        json with bird_code and imageUrl
    """
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            # user agent to avoid blocking
            page = await browser.new_page(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            try:
                image_url = await get_species_image_url(bird_code, browser_page=page)
                return {"birdCode": bird_code, "imageUrl": image_url}
            finally:
                await browser.close()
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"failed to fetch image: {str(e)}")
