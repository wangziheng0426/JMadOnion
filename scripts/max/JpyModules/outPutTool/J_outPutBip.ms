fn export_bip_fn =
  (
	path_S=inputPath
 
    select $Bip001
    
    biped.saveBipFile $.controller path_S
    
    
    
  )
export_bip_fn()