Includes = {
}

PixelShader =
{
	Samplers =
	{
		TextureOne =
		{
			Index = 0
			MagFilter = "Point"
			MinFilter = "Point"
			MipFilter = "None"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		TextureTwo =
		{
			Index = 1
			MagFilter = "Point"
			MinFilter = "Point"
			MipFilter = "None"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
	}
}


VertexStruct VS_INPUT
{
    float4 vPosition  : POSITION;
    float2 vTexCoord  : TEXCOORD0;
};

VertexStruct VS_OUTPUT
{
    float4  vPosition : PDX_POSITION;
    float2  vTexCoord0 : TEXCOORD0;
};


ConstantBuffer( 0, 0 )
{
	float4x4 WorldViewProjectionMatrix;
	float4 vFirstColor;
	float4 vSecondColor;
	float CurrentState;
};


VertexShader =
{
	MainCode VertexShader
	[[

		VS_OUTPUT main(const VS_INPUT v )
		{
			VS_OUTPUT Out;
		   	Out.vPosition  = mul( WorldViewProjectionMatrix, v.vPosition );
			Out.vTexCoord0  = v.vTexCoord;
			Out.vTexCoord0.y = -Out.vTexCoord0.y;

			return Out;
		}

	]]
}

PixelShader =
{
	MainCode PixelColor
	[[

		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
			float x = v.vTexCoord0.x;

			// Cumulative thresholds:
			//   vFirstColor.r  = end of party 0 (far_left)
			//   vFirstColor.g  = end of party 1 (left)
			//   vFirstColor.b  = end of party 2 (center_left)
			//   vFirstColor.a  = end of party 3 (center)
			//   vSecondColor.r = end of party 4 (center_right)
			//   vSecondColor.g = end of party 5 (right)
			//   party 6 (far_right) fills the remainder

			// Ideology colors from common/ideologies/00_ideologies.txt (RGB 0-1)
			if( x <= vFirstColor.r )
				return float4( 0.545, 0.000, 0.000, 1.0 );  // far_left:     rgb(139,  0,  0)
			if( x <= vFirstColor.g )
				return float4( 0.729, 0.141, 0.267, 1.0 );  // left:         rgb(186, 36, 68)
			if( x <= vFirstColor.b )
				return float4( 0.839, 0.376, 0.596, 1.0 );  // center_left:  rgb(214, 96,152)
			if( x <= vFirstColor.a )
				return float4( 0.831, 0.518, 0.125, 1.0 );  // center:       rgb(212,132, 32)
			if( x <= vSecondColor.r )
				return float4( 0.471, 0.659, 0.769, 1.0 );  // center_right: rgb(120,168,196)
			if( x <= vSecondColor.g )
				return float4( 0.361, 0.463, 0.580, 1.0 );  // right:        rgb( 92,118,148)

			return float4( 0.165, 0.188, 0.314, 1.0 );      // far_right:    rgb( 42, 48, 80)
		}

	]]

	MainCode PixelTexture
	[[

		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
			float x = v.vTexCoord0.x;
			float4 vTex = tex2D( TextureOne, v.vTexCoord0.xy );

			if( x <= vFirstColor.r )
				return vTex * float4( 0.545, 0.000, 0.000, 1.0 );
			if( x <= vFirstColor.g )
				return vTex * float4( 0.729, 0.141, 0.267, 1.0 );
			if( x <= vFirstColor.b )
				return vTex * float4( 0.839, 0.376, 0.596, 1.0 );
			if( x <= vFirstColor.a )
				return vTex * float4( 0.831, 0.518, 0.125, 1.0 );
			if( x <= vSecondColor.r )
				return vTex * float4( 0.471, 0.659, 0.769, 1.0 );
			if( x <= vSecondColor.g )
				return vTex * float4( 0.361, 0.463, 0.580, 1.0 );

			return vTex * float4( 0.165, 0.188, 0.314, 1.0 );
		}

	]]
}


BlendState BlendState
{
	BlendEnable = yes
	SourceBlend = "SRC_ALPHA"
	DestBlend = "INV_SRC_ALPHA"
}


Effect Color
{
	VertexShader = "VertexShader"
	PixelShader = "PixelColor"
}

Effect Texture
{
	VertexShader = "VertexShader"
	PixelShader = "PixelTexture"
}
