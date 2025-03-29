create or replace function
  `mdl.nfltouchdown_cloudrun` (
    input json
) returns json 
  remote with connection `australia-southeast1.cloudrun` 
  options (
    endpoint = '${cloud_run_url}'
  )
;