#######################################
# Name: Argon
#   Argument and  and configuration management helper functions
#   Noble like the gas
# Authors: ["Christopher Mortimer <christopher@mortimer.xyz>"]
#######################################

#######################################
# Parse a YAML configuration file and return key value pairs.
# Arguments:
#   filename: name of a yaml configuration parameter file
#   env: the environment, dev, ppd, prd
#   prefix: a prefix for the resolving variable names
# Returns
#   key="value"
# Usage after source:
#   eval $(parse_configuration config.yaml)
#   echo $variable
#######################################
function parse_config() {
   local filename=$1
   local env=$2

   # Can be passed to add a prefix to all variables
   local prefix=$3
   local s='[[:space:]]*' w='[a-zA-Z0-9_]*' fs=$(echo @ | tr @ '\034')
   sed -ne "s|^\($s\):|\1|" \
      -e "s|^\($s\)\($w\)$s:$s[\"']\(.*\)[\"']$s\$|\1$fs\2$fs\3|p" \
      -e "s|^\($s\)\($w\)$s:$s\(.*\)$s\$|\1$fs\2$fs\3|p" $1 |
      sed "s|<env>|$env|g" |
      sed "s|<netenv>|$netenv|g" |
      awk -F$fs '{
      indent = length($1)/2;
      vname[indent] = $2;
      for (i in vname) {if (i > indent) {delete vname[i]}}
      if (length($3) > 0) {
         vn=""; for (i=0; i<indent; i++) {vn=(vn)(vname[i])("_")}
         printf("%s%s%s=\"%s\"\n", "'$prefix'",vn, $2, $3);
      }
   }'
}

#######################################
# Parse a arguments to a shell script
# Arguments:
#   -e | --env: the environment, dev, prd
#   -n | --name: the name of the job
# Returns
#   none
# Usage:
#   parse_args "$@"
#######################################
function parse_args() {
   POSITIONAL=()
   while [[ $# -gt 0 ]]; do
      key="$1"

      case $key in
      -e | --env)
         env="$2"
         shift # past argument
         shift # past value
         ;;
      -n | --name)
         name="$2"
         shift # past argument
         shift # past value
         ;;
      *)                    # unknown option
         POSITIONAL+=("$1") # save it in an array for later
         shift              # past argument
         ;;
      esac
   done
   set -- "${POSITIONAL[@]}" # restore positional parameters

   echo env = "${env}"
}

#######################################
# Create a new config file with environment
# Arguments:
#   env: the environment, dev, ppd, prd
# Returns
#   none
# Usage:
#   config_env_file ppd
#######################################
config_env_file() {
   local env="$1"
   local config_path="$2"

   # Check if the configuration file exists
   if [ ! -f "${config_path}config.yaml" ]; then
      echo "Error: Configuration file not found: config.yaml"
      exit 1
   fi

   # Perform the replacement using sed
   sed -e "s/<env>/${env}/" "${config_path}config.yaml" > "config-${env}.yaml"

   echo "Replacement complete. New file: config-${env}.yaml"
}

function ansi_color_codes() {
   # Reset
   Color_Off='\033[0m'       # Text Reset

   # Regular Colors
   Black='\033[0;30m'        # Black
   Red='\033[0;31m'          # Red
   Green='\033[0;32m'        # Green
   Yellow='\033[0;33m'       # Yellow
   Blue='\033[0;34m'         # Blue
   Purple='\033[0;35m'       # Purple
   Cyan='\033[0;36m'         # Cyan
   White='\033[0;37m'        # White

   # Bold
   BBlack='\033[1;30m'       # Black
   BRed='\033[1;31m'         # Red
   BGreen='\033[1;32m'       # Green
   BYellow='\033[1;33m'      # Yellow
   BBlue='\033[1;34m'        # Blue
   BPurple='\033[1;35m'      # Purple
   BCyan='\033[1;36m'        # Cyan
   BWhite='\033[1;37m'       # White

   # Underline
   UBlack='\033[4;30m'       # Black
   URed='\033[4;31m'         # Red
   UGreen='\033[4;32m'       # Green
   UYellow='\033[4;33m'      # Yellow
   UBlue='\033[4;34m'        # Blue
   UPurple='\033[4;35m'      # Purple
   UCyan='\033[4;36m'        # Cyan
   UWhite='\033[4;37m'       # White

   # Background
   On_Black='\033[40m'       # Black
   On_Red='\033[41m'         # Red
   On_Green='\033[42m'       # Green
   On_Yellow='\033[43m'      # Yellow
   On_Blue='\033[44m'        # Blue
   On_Purple='\033[45m'      # Purple
   On_Cyan='\033[46m'        # Cyan
   On_White='\033[47m'       # White

   # High Intensity
   IBlack='\033[0;90m'       # Black
   IRed='\033[0;91m'         # Red
   IGreen='\033[0;92m'       # Green
   IYellow='\033[0;93m'      # Yellow
   IBlue='\033[0;94m'        # Blue
   IPurple='\033[0;95m'      # Purple
   ICyan='\033[0;96m'        # Cyan
   IWhite='\033[0;97m'       # White

   # Bold High Intensity
   BIBlack='\033[1;90m'      # Black
   BIRed='\033[1;91m'        # Red
   BIGreen='\033[1;92m'      # Green
   BIYellow='\033[1;93m'     # Yellow
   BIBlue='\033[1;94m'       # Blue
   BIPurple='\033[1;95m'     # Purple
   BICyan='\033[1;96m'       # Cyan
   BIWhite='\033[1;97m'      # White

   # High Intensity backgrounds
   On_IBlack='\033[0;100m'   # Black
   On_IRed='\033[0;101m'     # Red
   On_IGreen='\033[0;102m'   # Green
   On_IYellow='\033[0;103m'  # Yellow
   On_IBlue='\033[0;104m'    # Blue
   On_IPurple='\033[0;105m'  # Purple
   On_ICyan='\033[0;106m'    # Cyan
   On_IWhite='\033[0;107m'   # White
}
