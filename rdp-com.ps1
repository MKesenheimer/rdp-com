# Import-Module .\rdp-com.ps1 -force; rdp-com -delay 100 -pack 8 -path <filename>

Function Write-Bit {
	param($bit)
	#$bit = "a"
	# Write-Host $bit -NoNewLine
	if ($bit -eq '0')
		{Write-Host " " -NoNewLine -BackgroundColor Black}
	elseif ($bit -eq '1')
		{Write-Host " " -NoNewLine -BackgroundColor Red}
	elseif ($bit -eq '2')
		{Write-Host " " -NoNewLine -BackgroundColor Green}
	elseif ($bit -eq '3')
		{Write-Host " " -NoNewLine -BackgroundColor Yellow}
	elseif ($bit -eq '4')
		{Write-Host " " -NoNewLine -BackgroundColor Blue}
	elseif ($bit -eq '5')
		{Write-Host " " -NoNewLine -BackgroundColor Magenta}
	elseif ($bit -eq '6')
		{Write-Host " " -NoNewLine -BackgroundColor Cyan}
	elseif ($bit -eq '7')
		{Write-Host " " -NoNewLine -BackgroundColor White}
	elseif ($bit -eq '8')
		{Write-Host " " -NoNewLine -BackgroundColor DarkGray}
	elseif ($bit -eq '9')
		{Write-Host " " -NoNewLine -BackgroundColor DarkRed}
	elseif ($bit -eq 'a')
		{Write-Host " " -NoNewLine -BackgroundColor DarkGreen}
	elseif ($bit -eq 'b')
		{Write-Host " " -NoNewLine -BackgroundColor DarkYellow}
	elseif ($bit -eq 'c')
		{Write-Host " " -NoNewLine -BackgroundColor DarkBlue}
	elseif ($bit -eq 'd')
		{Write-Host " " -NoNewLine -BackgroundColor DarkMagenta}
	elseif ($bit -eq 'e')
		{Write-Host " " -NoNewLine -BackgroundColor DarkCyan}
	elseif ($bit -eq 'f')
		{Write-Host " " -NoNewLine -BackgroundColor Gray}
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
		$binary  = [System.Text.Encoding]::Default.GetBytes($content) | %{[convert]::ToString($_,16).PadLeft(2,'0')}
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
			Write-Byte -byte $byte.PadRight(2 * $pack, '0')
			# Clock-bit on
			Write-Host " " -BackgroundColor Black
			Start-Sleep -Milliseconds $delay
			
			Write-Byte -byte $byte.PadRight(2 * $pack, '0')
			# Clock-bit on
			Write-Host " " -BackgroundColor White
			Start-Sleep -Milliseconds $delay
		}
	}
}