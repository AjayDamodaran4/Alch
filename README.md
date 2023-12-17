WORKFLOW


1. check if any automation container is running already, if running use this by its standard name
2. if it's not running, initiate a container using docker compose-up
3. check if the container is up by verifying messages in logs
4. trigger simulator using command
5. check if the simulator run is finished by verifying messages in logs
6. fetch the transaction number
7. check if all four files are present if study is success
8. check if 3 files is present for any other study status





pending discussions

api utils, separate file for storing endpoints, configuring it accordingly
docker_utils --> cross check all methods written, configurations done in conftest
input_path and output_path --  repetiting 

docker sdk
pytest BDD
poetry



24-11-2023
just trigger a container named aiservice with below mounts

/verification/testdata/cxr/validstudy_1AP,1PA,1LA/:/app/input 
-v /verification/prior_dir/:/app/prior 
-v /verification/temp_output:/app/temporary 
-v /verification/output/:/app/output 
-v /verification/jobconfig/1/config.json:/app/config.json

-e requestPort=7000 
-e TZ="Europe/Stockholm"
-e runMode = "auto"

after the above is run, write your actual test case
1. Verify the expected outputs
2. fhir validation required
3. result manifest status code/text
4. 






