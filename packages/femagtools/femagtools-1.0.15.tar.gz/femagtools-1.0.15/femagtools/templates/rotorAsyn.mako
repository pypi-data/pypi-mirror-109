

m.stator_diam     =      da2
m.inside_diam     =      dy2
m.airgap          =     ag
m.slot_bs2        =     ${model['slot_bs2']*1e3}
m.slot_hs2        =     ${model['slot_hs2']*1e3}
m.slot_b32        =     
m.slot_h32        =     
m.slot_b42        =     
m.slot_h42        =     
m.slot_b52        =     
m.slot_b62        =     
m.slot_h52        =     
m.slot_h62        =     
m.slot_h72        =     
--m.nodedist        =     
 
m.tot_num_sl      = ${model['num_slots']}
m.num_sl_gen      = m.tot_num_sl * m.num_sl_gen / m.tot_num_slot
                                  --    Number of teeth be generated            
m.zeroangl        = ${model['zeroangl']}
 
m.mcvkey_yoke =   'M330-50A'
 
pre_models("ROTOR_ASYN")                                       
