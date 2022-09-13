# Import-Module .\rdp-com.ps1 -force; rdp-com -delay 100 -pack 8 -path <filename>

Function Write-Bit {
	param($bit)
	
	# Write-Host $bit -NoNewLine
	if ($bit -eq '1')
		{Write-Host " " -NoNewLine -BackgroundColor White}
	if ($bit -eq '0')
		{Write-Host " " -NoNewLine -BackgroundColor Black}
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
		$binary  = [System.Text.Encoding]::Default.GetBytes($content) | %{[convert]::ToString($_,2).PadLeft(8,'0')}
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
	
		#Write-Host $binary2
		
		#Write-Host (" "*($pack*8 + 1)) -BackgroundColor Black
		#Start-Sleep -Milliseconds $delay
		#Write-Host (" "*($pack*8 + 1)) -BackgroundColor White
		#Start-Sleep -Milliseconds $delay
			
		Foreach($byte in $binary2.split()) {
			Write-Byte -byte $byte.PadRight(8 * $pack, ' ')
			# Clock-bit on
			Write-Host " " -BackgroundColor Black
			Start-Sleep -Milliseconds $delay
			
			Write-Byte -byte $byte.PadRight(8 * $pack, ' ')
			# Clock-bit on
			Write-Host " " -BackgroundColor White
			Start-Sleep -Milliseconds $delay
		}
	}
}