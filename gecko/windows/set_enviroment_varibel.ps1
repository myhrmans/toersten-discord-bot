$desired_entry = $PSScriptRoot

$old_path = [Environment]::GetEnvironmentVariable('path', 'machine');

$old_path_entry_list = ($old_path).split(";")
$new_path_entry_list = new-object system.collections.arraylist

foreach($old_path_entry in $old_path_entry_list) {
    if($old_path_entry -eq $desired_entry){
        # ignore old entry
    }else{
        [void]$new_path_entry_list.Add($old_path_entry)
    }
}
[void]$new_path_entry_list.Add($desired_entry)
$new_path = $new_path_entry_list -Join ";"

[Environment]::SetEnvironmentVariable('path', $new_path,'Machine');