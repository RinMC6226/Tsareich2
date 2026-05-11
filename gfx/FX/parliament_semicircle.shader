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
			// UV: (0,0)=top-left, (1,1)=bottom-right
			// Semicircle center at bottom-center: (0.5, 1.0)
			float2 center = float2( 0.5f, 1.0f );
			float2 diff = v.vTexCoord0 - center;
			float dist = length( diff );

			// Arc band: inner radius 0.35, outer radius 0.95
			// CurrentState controls outer radius (default 0.95 if unused)
			float outerR = 0.95f;
			float innerR = 0.35f;
			if( dist < innerR || dist > outerR || diff.y > 0.0f )
				discard;

			// Angle: 0 (left) to PI (right)
			// atan2(-diff.x, -diff.y) gives 0 at bottom, going clockwise
			// We remap: left side of semicircle = 0, right side = 1
			float angle = atan2( -diff.x, -diff.y );
			float normalized = ( angle + 1.5707963f ) / 3.1415926f;
			normalized = saturate( normalized );

			// Cumulative thresholds (same encoding as parliament_bar)
			if( normalized <= vFirstColor.r )
				return float4( 0.545, 0.000, 0.000, 1.0 );  // far_left
			if( normalized <= vFirstColor.g )
				return float4( 0.729, 0.141, 0.267, 1.0 );  // left
			if( normalized <= vFirstColor.b )
				return float4( 0.839, 0.376, 0.596, 1.0 );  // center_left
			if( normalized <= vFirstColor.a )
				return float4( 0.831, 0.518, 0.125, 1.0 );  // center
			if( normalized <= vSecondColor.r )
				return float4( 0.471, 0.659, 0.769, 1.0 );  // center_right
			if( normalized <= vSecondColor.g )
				return float4( 0.361, 0.463, 0.580, 1.0 );  // right

			return float4( 0.165, 0.188, 0.314, 1.0 );      // far_right
		}

	]]

	MainCode PixelTexture
	[[

		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
			float2 center = float2( 0.5f, 1.0f );
			float2 diff = v.vTexCoord0 - center;
			float dist = length( diff );

			float outerR = 0.95f;
			float innerR = 0.35f;
			if( dist < innerR || dist > outerR || diff.y > 0.0f )
				discard;

			float angle = atan2( -diff.x, -diff.y );
			float normalized = ( angle + 1.5707963f ) / 3.1415926f;
			normalized = saturate( normalized );

			float4 vTex = tex2D( TextureOne, v.vTexCoord0.xy );

			if( normalized <= vFirstColor.r )
				return vTex * float4( 0.545, 0.000, 0.000, 1.0 );
			if( normalized <= vFirstColor.g )
				return vTex * float4( 0.729, 0.141, 0.267, 1.0 );
			if( normalized <= vFirstColor.b )
				return vTex * float4( 0.839, 0.376, 0.596, 1.0 );
			if( normalized <= vFirstColor.a )
				return vTex * float4( 0.831, 0.518, 0.125, 1.0 );
			if( normalized <= vSecondColor.r )
				return vTex * float4( 0.471, 0.659, 0.769, 1.0 );
			if( normalized <= vSecondColor.g )
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
