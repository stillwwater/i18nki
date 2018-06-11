read -d '' DOC <<- EOF
bench.sh [-h|--help] [-k|--keys] [-c|--clean]
--help     : show this message
--keys     : number of keys to generate and benchmark
--clean    : remove temp files after executing
--compiler : change compiler for i18nki
EOF

POSITIONAL=()
COMPILER=ini

while [[ $# -gt 0 ]]; do
  key=$1
  case $key in
    -k|--keys)
      KEYCOUNT=$2
      shift # key
      shift # value
      ;;
    -c|--clean)
      CLEAN=True
      shift
      ;;
    --compiler)
      COMPILER=$2
      shift
      shift
      ;;
    -h|--help)
      echo "$DOC"
      exit
      ;;
    *)
      break
      ;;
  esac
done

set -- POSITIONAL[@]

if [ -f tmp/out ]; then
  rm tmp/out
fi

mkdir tmp
python3 gen_data.py $KEYCOUNT
cd ..
python3 -m i18nki -i benchmark/tmp -o benchmark/tmp/out -f '.*?_\((.*?)\).*?$' -c '//' --compiler $COMPILER
cd benchmark

if [ -z $CLEAN ]; then
  exit
fi

rm tmp/out
rm tmp/tmp
rmdir tmp
