jobid=$(ps -u | grep TeleTruck.py | grep -v "grep" | sed 's/\ \+/\ /g' | cut -d' ' -f2)
echo $jobid
kill $jobid
rm *.pyc

if [ "$1" = "force" ]
then
  jobid=$(ps -u | grep runspade.py | grep -v "grep" | sed 's/\ \+/\ /g' | cut -d' ' -f2)
  echo $jobid
  kill $jobid
fi
