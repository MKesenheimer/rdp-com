# Import-Module .\rdp-com.ps1 -force; rdp-com -delay 100 -pack 8 -path <filename>

Function Write-Bit {
	param($bit)
	#$bit = 7
	# Write-Host $bit -NoNewLine
	if ($bit -eq '0')
		{Write-Host " " -NoNewLine -BackgroundColor Black} # (0, 0, 0)
	if ($bit -eq '1')
		{Write-Host " " -NoNewLine -BackgroundColor Red} # (0, 0, 1)
	if ($bit -eq '2')
		{Write-Host " " -NoNewLine -BackgroundColor Green}  # (0, 1, 0)
	if ($bit -eq '3')
		{Write-Host " " -NoNewLine -BackgroundColor Yellow} # (0, 1, 1)
	if ($bit -eq '4')
		{Write-Host " " -NoNewLine -BackgroundColor Blue} # (1, 0, 0)
	if ($bit -eq '5')
		{Write-Host " " -NoNewLine -BackgroundColor Magenta}  # (1, 0, 1)
	if ($bit -eq '6')
		{Write-Host " " -NoNewLine -BackgroundColor Cyan} # (1, 1, 0)
	if ($bit -eq '7')
		{Write-Host " " -NoNewLine -BackgroundColor White} # (1, 1, 1)
}

Function Write-Byte {
	param($byte)
	Foreach ($bit in [char[]]$byte) {
		Write-Bit -bit $bit
	}
}

Function RDP-Com {
	param(
		[String][parameter(mandatory=$true, ValuefrompipeLine=$true)] $Path,
		[int][parameter(mandatory=$true, ValuefrompipeLine=$true)] $delay,
		[int][parameter(mandatory=$true, ValuefrompipeLine=$true)] $pack
	)
	
	Begin {
		# Write-Host $Path
		$content = [convert]::ToBase64String((Get-Content -path $Path -Encoding byte))
		# convert character string to value string in base 8
		#$content = "a"
		$binary  = [System.Text.Encoding]::Default.GetBytes($content) | %{[convert]::ToString($_,8).PadLeft(3,'0')}
	}

	Process {
		# pack bytes
		$count = 0
		$binary2 = ''
		Foreach ($byte in $binary.split()) {
			$binary2 += $byte
			$count++
			if ($count -eq $pack) {
				$binary2 += " "
				$count = 0
			}
		}
		$binary2 = $binary2.trim()
	
		Write-Host $binary2
		
		#Write-Host (" "*($pack*8 + 1)) -BackgroundColor Black
		#Start-Sleep -Milliseconds $delay
		#Write-Host (" "*($pack*8 + 1)) -BackgroundColor White
		#Start-Sleep -Milliseconds $delay
			
		Foreach($byte in $binary2.split()) {
			Write-Byte -byte $byte.PadRight(3 * $pack, '0')
			# Clock-bit on
			Write-Host " " -BackgroundColor Black
			Start-Sleep -Milliseconds $delay
			
			Write-Byte -byte $byte.PadRight(3 * $pack, '0')
			# Clock-bit on
			Write-Host " " -BackgroundColor White
			Start-Sleep -Milliseconds $delay
		}
	}
}