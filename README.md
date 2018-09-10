# PlanB
Simplifying the creation and backup of network shares

PlanB is used to simplify the creation of samba shares and backing up the contents of these shares.

Example:
You need to backup 10 different computers, each have their unique documents folder while all share a media folder.
Create a private share for each computer and one public share for the media
Set up a cron task or use Task Scheduler to sync the contents with the shares.
Setup backup locations on the Samba server, connect the backup disk and run the backup.