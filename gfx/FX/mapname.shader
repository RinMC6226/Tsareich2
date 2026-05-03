Includes = {
	"constants.fxh"
	"standardfuncsgfx.fxh"
}

PixelShader =
{
	Samplers =
	{
		DiffuseTexture =
		{
			Index = 0
			MipMapLodBias = -0.4
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "Linear"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
	}
}

		
ConstantBuffer( 1, 32 )
{
	float4 Transp_OffsetX;
};

VertexStruct VS_INPUT
{
    float3 vPosition  : POSITION;
	float2 vTexCoord  : TEXCOORD0;
};

VertexStruct VS_OUTPUT
{
    float4 vPosition : PDX_POSITION;
	float3 vPrepos   : TEXCOORD0;
    float2 vTexCoord : TEXCOORD1;
};


VertexShader =
{
	MainCode VertexShader
	[[
		VS_OUTPUT main( const VS_INPUT v )
		{
			VS_OUTPUT Out;
		
			float4 vPos = float4( v.vPosition, 1.0f );
			vPos.x += Transp_OffsetX.y;
			float4 vDistortedPos = vPos - float4( vCamLookAtDir * 0.5f, 0.0f );
		
			vPos = mul( ViewProjectionMatrix, vPos );
			
			// move z value slightly closer to camera to avoid intersections with terrain
			float vNewZ = dot( vDistortedPos, float4( GetMatrixData( ViewProjectionMatrix, 2, 0 ), GetMatrixData( ViewProjectionMatrix, 2, 1 ), GetMatrixData( ViewProjectionMatrix, 2, 2 ), GetMatrixData( ViewProjectionMatrix, 2, 3 ) ) );
			
			Out.vPosition = float4( vPos.xy, vNewZ, vPos.w );
			Out.vPrepos = v.vPosition.xyz;
			Out.vTexCoord = v.vTexCoord;
		
			return Out;
		}
		
		
	]]
}

PixelShader =
{
	MainCode PixelShader
	[[
		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
			float4 vSample = tex2D( DiffuseTexture, v.vTexCoord );
			float baseAlpha = vSample.a;
			vSample.a *= Transp_OffsetX.x * 0.5f;// * vFade;	
			vSample.rgb *= 1.05f;
			vSample.rgb *= 1.0f - ( DayNightFactor( CalcGlobeNormal( v.vPrepos.xz ) ) * 0.35f );
			float glowAlpha = 0.0f;
			float glowOpacity = 0.0f;
			float2 uvStep = clamp( fwidth( v.vTexCoord ) * 1.25f, float2( 0.00010f, 0.00010f ), float2( 0.00050f, 0.00050f ) );
			[unroll]
			for ( int i = 1; i <= 10; ++i )
			{
				float ring = (float)i;
				float t = ring / 10.0f;
				float scale = ring * 1.0f;
				float2 dir0 = float2( 1.0f, 0.0f );
				float2 dir1 = float2( 0.92387953f, 0.38268343f );
				float2 dir2 = float2( 0.70710678f, 0.70710678f );
				float2 dir3 = float2( 0.38268343f, 0.92387953f );
				float2 off0 = uvStep * dir0 * scale;
				float2 off1 = uvStep * dir1 * scale;
				float2 off2 = uvStep * dir2 * scale;
				float2 off3 = uvStep * dir3 * scale;
				float ringAlpha =
					tex2D( DiffuseTexture, v.vTexCoord + off0 ).a +
					tex2D( DiffuseTexture, v.vTexCoord - off0 ).a +
					tex2D( DiffuseTexture, v.vTexCoord + float2( off0.y, off0.x ) ).a +
					tex2D( DiffuseTexture, v.vTexCoord - float2( off0.y, off0.x ) ).a +
					tex2D( DiffuseTexture, v.vTexCoord + off1 ).a +
					tex2D( DiffuseTexture, v.vTexCoord - off1 ).a +
					tex2D( DiffuseTexture, v.vTexCoord + float2( off1.x, -off1.y ) ).a +
					tex2D( DiffuseTexture, v.vTexCoord + float2( -off1.x, off1.y ) ).a +
					tex2D( DiffuseTexture, v.vTexCoord + off2 ).a +
					tex2D( DiffuseTexture, v.vTexCoord - off2 ).a +
					tex2D( DiffuseTexture, v.vTexCoord + float2( off2.x, -off2.y ) ).a +
					tex2D( DiffuseTexture, v.vTexCoord + float2( -off2.x, off2.y ) ).a +
					tex2D( DiffuseTexture, v.vTexCoord + off3 ).a +
					tex2D( DiffuseTexture, v.vTexCoord - off3 ).a +
					tex2D( DiffuseTexture, v.vTexCoord + float2( off3.x, -off3.y ) ).a +
					tex2D( DiffuseTexture, v.vTexCoord + float2( -off3.x, off3.y ) ).a;
				ringAlpha *= 0.0625f;

				float ringGlow = saturate( ringAlpha - baseAlpha * ( 0.48f + t * 0.22f ) );
				float ringWeight = lerp( 0.32f, 0.06f, t );
				float alphaWeight = lerp( 0.1f, 0.015f, t );

				glowAlpha += ringGlow * ringWeight;
				glowOpacity += ringGlow * alphaWeight;
			}
			glowAlpha = saturate( glowAlpha );
			glowOpacity = saturate( glowOpacity );
			vSample.rgb = lerp( vSample.rgb, float3( 1.0f, 1.0f, 1.0f ), glowAlpha * 0.82f );
			vSample.a = saturate( vSample.a + glowOpacity * Transp_OffsetX.x );
			return vSample;
		}
	]]
}


BlendState BlendState
{
	BlendEnable = yes
	AlphaTest = no
	SourceBlend = "src_alpha"
	DestBlend = "inv_src_alpha"
	WriteMask = "RED|GREEN|BLUE"
}

DepthStencilState DepthStencilState
{
	DepthEnable = no
	DepthWriteMask = "depth_write_all"
	DepthFunction = "comparison_less_equal"
	StencilEnable = yes
	FrontStencilFailOp = "stencil_op_keep"
	FrontStencilDepthFailOp = "stencil_op_keep"
	FrontStencilPassOp = "stencil_op_keep"
	FrontStencilFunc = "comparison_not_equal"
	StencilRef = 4
	StencilReadMask = 4
}


Effect mapname
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShader"
	DepthStencilState = "DepthStencilState"
}
