#!/bin/bash
file=location_codes.txt
i=1
start=133
while read line ; do
	if [ $i -gt $start ] ; then
		echo "Line No $i: $line"
		instaloader --login=sociopatito --post-filter="date_utc >=datetime(2022,1,1) and date_utc < datetime(2023,1,1)" %$line  --no-profile-pic --no-videos --post-metadata-txt="{mediaid}, {shortcode},{title},{owner_profile},{owner_id},{date_local},{url}, {likes}, {comments}, {caption}, {profile}, {location}" --no-metadata-json --fast-update --count 500 --abort-on 429
		sleep 400
	fi
i=$((i+1))
done < $file
