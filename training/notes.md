# Warframe Assist App
Assists in warframe game without injecting any code. instead uses screen captures, neural networks and macros. 
# Features

## Screen capture and value extraction:
---
- ### Health and shields states for self, companion, squadmates:
    Gets shields (if any) and health from a screen capture and turns it to a numerical value and states such as :
    - ### Normal:  
        - Shields and health are in a damageable state.  
        - This is the most common state.  
        - <span style="color:rgb(0, 255, 255)">Shield RGB8: [0, 255, 255] (cyan)</span>
        - <span style="color:rgb(255, 49, 65)">Health RGB8: [255, 49, 65] (red)</span>
    - ### Overshields:  
        - Like normal but shield number is purple and beyond the "max" shield value.
        - <span style="color:rgb(255, 0, 255)">Overshields RGB8: [255, 0, 255] (magenta)</span>
    - ### No shields:
        - Has no shield value at all
        - Happens for Operator and some warframes like nidus and inaros.
    - ### Invulnerable:  
        - Cannot take damage, shield (if any) and health become diffrent colored grey, 
        - Health and shield values are not important here but might still be interesting because you can still heal.
        - <span style="color:rgb(255, 255, 255)">Shield RGB8: [255, 255, 255] (white)</span>
        - <span style="color:rgb(170, 170, 170)">Health RGB8: [170, 170, 170] (dark grey)</span>
    - ### Dead:  
        - Red text saying "DEAD"
        - Same color as health
    - ### Scrambled (maybe):
        - Scrambled the image making it useless
        - Happens during magnetic procs  

    Loss should be increasing for each digit that is wrong, not linear for total value.  
    Crop out the little bar under values.  
    Maybe apply proccessing to images to bias known colors  
    - ### Rectangels
      - name: [x, y, w, h]
      - player: [3481, 58, 305, 58~59]
      - companion:
      - squadmate1:
      - squadmate2:
      - squadmate3:
      - objective:

---
- ### Energy for self
   numerical current energy value
---
- ### Energy for squadmates
    0 to 100% current energy 
---
- ### Squadmates in Affinity range
    Check status effects for affinity range on squadmates
<!--- 
<span style="color:rgb(0, 255, 255)">some *blue* text</span> 
--->