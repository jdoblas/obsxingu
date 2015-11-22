def maskCloudsAndSuch(img):
  import ee    
  #Bust clouds
  def cloudScore(img):
    # A helper to apply an expression and linearly rescale the output.
    def rescale (img, thresholds):
      return img.subtract(thresholds[0]).divide(thresholds[1] - thresholds[0])
    # Compute several indicators of cloudyness and take the minimum of them.
    score = ee.Image(1.0)
    soma=ee.Image(1.0)
    # Clouds are reasonably bright in the blue band.
    score = score.min(rescale(img.select('blue'), [0.1, 0.3]))    
    # Clouds are reasonably bright in all visible bands.
    soma=img.select('red').add(img.select('green')).add(img.select('blue'))
    score=score.min(rescale(soma, [0.2, 0.8]))
    # Clouds are reasonably bright in all infrared bands.
    soma=img.select('nir').add(img.select('swir1')).add(img.select('swir2'))
    score=score.min(rescale(soma, [0.3, 0.8]))
    # Clouds are reasonably cool in temperature.
    score = score.min(rescale(img.select('temp'), [300, 290]))
  
    return img.addBands(score).select([0],['cloud'])

  cs = cloudScore(img).select(['cloud']).gt(img.select(['cloudThresh']))
#    numberBandsHaveData = img.mask().reduce(ee.Reducer.sum())
#    allOrNoBandsHaveData = numberBandsHaveData.eq(0).or(numberBandsHaveData.gte(8))
#    allBandsHaveData = allOrNoBandsHaveData
#    allBandsGT = img.reduce(ee.Reducer.min()).gt(-0.001)
#    return img.mask(img.mask().and(cs.not()).and(allBandsHaveData).and(allBandsGT))
  return img.mask(cs.Not())

def maskShadows(col):
  import ee
  #RSAC_Temporal_Dark_Outlier_Mask(TDOM) by Carson Stam
  shadowSumBands=['red','swir1','swir2']
  def addShadowSum(img):
    return img.addBands(img.select(shadowSumBands).reduce(ee.Reducer.sum()).select([0],['shadowSum']))
  def zShadowMask(img,meanShadowDark,stdShadowDark):
    imgDark = img.select(['shadowSum'])
    shadowZ = imgDark.subtract(meanShadowDark).divide(stdShadowDark)
    shadows = shadowZ.lt(img.select(['zShadowThresh']))
    return img.mask(img.mask().And(shadows.Not()))
  def help_f(img):
    return zShadowMask(img,meanShadowSum,stdShadowSum)
  
  #add shadowsum band
  colSS =  col.map(addShadowSum)
  #Compute stats for dark pixels for shadow masking
  meanShadowSum = colSS.select(['shadowSum']).mean()
  stdShadowSum = colSS.select(['shadowSum']).reduce(ee.Reducer.stdDev())
  #Apply z score shadow method
  colSS = colSS.map(help_f)
  return colSS




